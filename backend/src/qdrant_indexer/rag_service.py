import os
import logging
from typing import List, Dict, Any

import google.generativeai as genai
from dotenv import load_dotenv

from .qdrant_service import QdrantService
from .text_processor import TextProcessor

load_dotenv()
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, qdrant_service: QdrantService, text_processor: TextProcessor):
        self.qdrant_service = qdrant_service
        self.text_processor = text_processor
        self.gemini_model = os.getenv("GEMINI_RAG_MODEL", "gemini-pro") # Use gemini-pro for RAG
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {} # In-memory storage for session history
        self._init_gemini_rag_model()

    def _init_gemini_rag_model(self):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            # Test model availability
            genai.GenerativeModel(self.gemini_model)
            logger.info(f"Initialized Google Gemini RAG model: {self.gemini_model}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Gemini RAG model: {e}")
            raise

    def query_rag(self, query: str, rag_session_id: str = None, top_k: int = 5) -> str:
        """
        Processes a user query using RAG:
        1. Embeds the query.
        2. Searches Qdrant for relevant documents.
        3. Constructs a prompt with retrieved context.
        4. Generates an answer using Google Gemini Pro.
        """
        logger.info(f"Received RAG query: {query}")

        # 1. Embed the query
        try:
            query_embedding = self.text_processor.get_embeddings(
                [query], task_type="retrieval_query"
            )[0]
        except Exception as e:
            logger.error(f"Failed to generate embedding for query: {e}")
            return "Error: Could not process query embedding."

        # 2. Search Qdrant for relevant documents
        try:
            search_results = self.qdrant_service.search(
                query_vector=query_embedding,
                limit=top_k
            )
            
            # Debugging search results
            logger.debug(f"Qdrant search_results type: {type(search_results)}")
            logger.debug(f"Qdrant search_results.points count: {len(search_results.points)}")
            if not search_results.points:
                logger.warning("No relevant points found in Qdrant for the query.")
                return "No relevant information found in the knowledge base."
            
            retrieved_texts = [result.payload.get("text", "") for result in search_results.points if result.payload]
            
            # Debugging retrieved texts and context
            logger.debug(f"Retrieved texts count: {len(retrieved_texts)}")
            logger.debug(f"First retrieved text: {retrieved_texts[0][:100]}..." if retrieved_texts else "No retrieved texts.")
            context = "\n\n".join(retrieved_texts)
            logger.debug(f"Constructed context length: {len(context)}")

        except Exception as e:
            logger.error(f"Failed to search Qdrant: {e}", exc_info=True) # Log full exception info
            return "Error: Could not retrieve information from the knowledge base."

        # 3. Construct a prompt with retrieved context and conversation history
        conversation_history = self.conversation_histories.get(rag_session_id, []) if rag_session_id else []
        
        history_str = ""
        if conversation_history:
            history_str = "\n".join([f"User: {turn['user']}\nAssistant: {turn['assistant']}" for turn in conversation_history])
            history_str = f"\n\nConversation History:\n{history_str}\n"

        prompt = f"""
        You are an AI assistant specialized in answering questions based on provided documentation.
        Use only the information from the following context to answer the question.
        If the answer cannot be found in the context, respond with "I cannot answer this question based on the provided information."
        
        {history_str}

        Context:
        {context}

        Question: {query}

        Answer:
        """
        logger.debug(f"Prompt sent to Gemini:\n{prompt}")

        # 4. Generate an answer using Google Gemini Pro
        try:
            model = genai.GenerativeModel(self.gemini_model, generation_config=self.generation_config)
            response = model.generate_content(prompt)
            answer = response.text
            
            if rag_session_id:
                if rag_session_id not in self.conversation_histories:
                    self.conversation_histories[rag_session_id] = []
                self.conversation_histories[rag_session_id].append({"user": query, "assistant": answer})
                
            return answer
        except Exception as e:
            logger.error(f"Failed to generate answer from Gemini Pro: {e}")
            return "Error: Could not generate an answer."
