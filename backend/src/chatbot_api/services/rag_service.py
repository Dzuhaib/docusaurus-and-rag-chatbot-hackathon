from . import gemini_service
from . import qdrant_service
from ..config import settings
from typing import Optional, Tuple, List, Dict, Union, AsyncIterator
import json # Import json for streaming

def _build_prompt(query: str, retrieved_context: list[dict], history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Constructs a prompt for the generative model, using retrieved documents as context
    and optionally conversation history, to answer the user's query.
    """
    context_text = "\n\n".join([doc.get("text", "") for doc in retrieved_context if doc.get("text")])
    
    # Format history into a string
    history_text = ""
    if history:
        for turn in history:
            history_text += f"{turn['sender']}: {turn['text']}\n"
        history_text += "\n" # Add a newline for separation

    return (
        f"You are a helpful assistant. Answer the user's question based ONLY on the following context:\n\n"
        f"--- CONTEXT ---\n{context_text}\n--- END CONTEXT ---\n\n"
        f"--- CONVERSATION HISTORY ---\n{history_text}--- END CONVERSATION HISTORY ---\n\n"
        f"Question: {query}\n\n"
        f"If the answer is not available in the context, state that you cannot answer from the provided text.\n"
        f"Answer:"
    )

async def get_rag_response( # Changed to async def
    query: str, 
    top_k: int = 3, 
    context: Optional[str] = None, 
    history: Optional[List[Dict[str, str]]] = None,
    stream: bool = False
) -> AsyncIterator[str]: # Now always yields JSON strings
    """
    Orchestrates the RAG process.
    - Always yields JSON-formatted chunks for consistent handling by main.py.
    - If 'stream' is False, main.py will collect these chunks and build a final ChatResponse.
    """
    try:
        llm_service = gemini_service

        search_text = context if context else query
        
        query_embedding = llm_service.get_embedding(search_text)
        if not query_embedding:
            yield json.dumps({"type": "error", "content": "Could not generate embedding for your query."}) + "\n"
            return # Exit generator

        retrieved_documents = qdrant_service.search_documents(query_embedding, top_k)

        sources = []
        if not retrieved_documents:
            error_message = "I can only answer questions related to the content of the book. Please ask a question about the book."
            yield json.dumps({"type": "error", "content": error_message}) + "\n"
            return # Exit generator
        
        unique_sources = {}
        for doc in retrieved_documents:
            if doc.get("url"):
                unique_sources[doc["url"]] = {
                    "url": doc["url"],
                    "page_title": doc.get("page_title", "Unknown Source")
                }
        sources = list(unique_sources.values())
        
        final_prompt = _build_prompt(query, retrieved_documents, history)
        
        # Always yield sources first, even for non-streaming, so main.py can collect it
        yield json.dumps({"type": "sources", "content": sources}) + "\n"

        if stream:
            # Yield content chunks from the generative model directly
            async for chunk in await llm_service.generate_content(final_prompt, stream=True):
                yield json.dumps({"type": "chunk", "content": chunk}) + "\n"
        else:
            # Non-streaming: Collect full response and then yield it as a single 'response' type
            full_response_text = ""
            async for chunk in await llm_service.generate_content(final_prompt, stream=True):
                full_response_text += chunk
            yield json.dumps({"type": "response", "content": full_response_text}) + "\n" # Single response chunk

    except Exception as e:
        print(f"Error in RAG process: {e}")
        yield json.dumps({"type": "error", "content": f"An error occurred while processing your request: {e}"}) + "\n"
        return # Exit generator
