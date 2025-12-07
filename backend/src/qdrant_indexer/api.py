import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .qdrant_service import QdrantService
from .text_processor import TextProcessor
from .rag_service import RAGService

load_dotenv()
logger = logging.getLogger(__name__)

# Configure logging (similar to main.py)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Docusaurus frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for request bodies
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5 # Default top_k value

class ChatkitRAGRequest(BaseModel):
    rag_session_id: str
    message: str

# Dependency injection for services (instantiate once)
# This will be created when the FastAPI app starts up
@app.on_event("startup")
async def startup_event():
    global qdrant_service, text_processor, rag_service
    try:
        qdrant_service = QdrantService()
        text_processor = TextProcessor(docs_base_path=os.path.join("..", "..", "book-site", "docs"))
        rag_service = RAGService(qdrant_service=qdrant_service, text_processor=text_processor)
        logger.info("FastAPI RAG services initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize RAG services: {e}")
        # Optionally re-raise or handle more gracefully depending on desired startup behavior
        raise e

import uuid

@app.get("/")
async def read_root():
    return {"message": "RAG API is running!"}

@app.post("/api/chatkit/session-init")
async def chatkit_session_init():
    session_id = str(uuid.uuid4())
    return JSONResponse(content={"rag_session_id": session_id})


@app.post("/query")
async def rag_query_endpoint(request: QueryRequest):
    try:
        user_query = request.query
        top_k = request.top_k
        
        answer = rag_service.query_rag(query=user_query, top_k=top_k)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        logger.error(f"Error processing RAG query: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/chatkit/rag-chat")
async def chatkit_rag_endpoint(request: ChatkitRAGRequest):
    try:
        user_message = request.message
        rag_session_id = request.rag_session_id
        
        # In a real scenario, rag_session_id would be used to manage conversation history
        # For now, we'll just pass the message to the RAG service
        answer = rag_service.query_rag(query=user_message, top_k=5) # Using default top_k for chat
        
        return JSONResponse(content={"rag_session_id": rag_session_id, "response": answer})
    except Exception as e:
        logger.error(f"Error processing Chatkit RAG query for session {rag_session_id}: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)