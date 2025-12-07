from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse # Import StreamingResponse
from .config import settings
from .models.chat_models import ChatRequest, ChatResponse, FeedbackRequest
from .services import rag_service
import json
from pathlib import Path
import datetime

app = FastAPI(
    title="RAG Chatbot API",
    description="API for the Retrieval Augmented Generation Chatbot using Gemini and Qdrant."
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a path for the feedback log file
FEEDBACK_FILE = Path("feedback_log.json")

@app.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "ok"}

@app.post("/chat") # Removed response_model to handle both StreamingResponse and ChatResponse
async def chat_endpoint(request: ChatRequest, fastapi_request: Request):
    """
    Endpoint for handling chat queries, now supporting streaming responses.
    """
    stream_response = fastapi_request.headers.get("X-Stream-Response") == "true"

    try:
        if stream_response:
            async def generate_stream_content():
                async for chunk_json in rag_service.get_rag_response(
                    query=request.query, 
                    context=request.context, 
                    history=request.history,
                    stream=True
                ):
                    yield chunk_json.encode("utf-8") # Yield bytes
            
            return StreamingResponse(generate_stream_content(), media_type="application/x-ndjson")
        else:
            response_content, sources = rag_service.get_rag_response(
                query=request.query, 
                context=request.context,
                history=request.history,
                stream=False
            )
            # The ChatResponse model will automatically generate a message_id
            return ChatResponse(response=response_content, sources=sources)
    except Exception as e:
        # For non-streaming, raise HTTP exception directly
        if not stream_response:
            raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
        # For streaming, yield an error message
        async def generate_error_stream():
            yield json.dumps({"type": "error", "content": f"Internal server error: {e}"}).encode("utf-8") + b"\n"
        return StreamingResponse(generate_error_stream(), media_type="application/x-ndjson")


@app.post("/feedback", status_code=204)
async def feedback_endpoint(request: FeedbackRequest):
    """
    Endpoint for receiving user feedback on a response.
    """
    try:
        feedback_data = request.model_dump()
        feedback_data["timestamp"] = datetime.datetime.utcnow().isoformat()
        
        # Read existing data, append new feedback, and write back
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, "r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(feedback_data)
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(FEEDBACK_FILE, "w") as f:
                json.dump([feedback_data], f, indent=4)

    except Exception as e:
        # Log the error, but don't prevent the user from getting a response
        print(f"Error saving feedback: {e}")
        # We don't raise an HTTPException here because feedback failing is not critical to the user's flow
    return

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
