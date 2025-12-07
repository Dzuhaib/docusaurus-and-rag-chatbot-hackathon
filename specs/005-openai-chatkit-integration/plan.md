---
id: 05
title: Plan for FastAPI Backend with Chatkit and Gemini Embeddings
stage: plan
date: 2025-12-06
model: Gemini 1.5 Flash
feature: openai-chatkit-integration
branch: main
user: current_user
command: "create plan for FastAPI Chatkit Backend using gemini-embedding-001"
labels: ["backend", "fastapi", "chatkit", "gemini", "qdrant", "plan", "rag"]
links:
  spec: specs/005-openai-chatkit-integration/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/005-openai-chatkit-integration/plan.md
tests_yaml: []
prompt_text: "Let's do Backend: FastAPI (using Chatkit.js and Chatkit.py, though this was later refined/questioned regarding its role with OpenAI). create constitution first, specify then, plan, tasks. and use gemini-embedding-001 instead of embedding-001"
response_text: "Plan created for the FastAPI Backend with Chatkit integration and gemini-embedding-001."
outcome: "Plan created successfully."
evaluation: "The plan details the implementation strategy for the FastAPI backend, including folder structure, key modules, dependencies, and integration with external services."
---
# Plan for FastAPI Backend with Chatkit and Gemini Embeddings

## 1. High-Level Design Refinement
The FastAPI application will be structured to facilitate clear separation of concerns and maintainability.
*   **Main Application (`main.py`):** Will host the FastAPI app instance, define API routes, and handle dependency injection for services.
*   **Configuration (`config.py`):** Responsible for loading environment variables and application settings.
*   **Services Layer:**
    *   `gemini_service.py`: Encapsulates all interactions with the Google Gemini API, including embedding generation (`gemini-embedding-001`) and conversational model calls.
    *   `qdrant_service.py`: Manages the connection and queries to the Qdrant vector database.
    *   `rag_service.py`: Orchestrates the RAG process: takes a user query, uses `gemini_service` for embedding, `qdrant_service` for retrieval, and then `gemini_service` again for generating the final response.
    *   `chat_service.py`: (Optional, depending on Chatkit.py features) Could manage basic chat history or conversational context if `Chatkit.py` doesn't provide it sufficiently. For initial implementation, `rag_service` will handle the core logic.
*   **Models Layer (`models/chat_models.py`):** Defines Pydantic models for request and response validation and serialization.

## 2. Folder Structure
The new backend components will reside under `backend/src/chatbot_api/`.

```
backend/
└── src/
    ├── qdrant_indexer/ (existing)
    └── chatbot_api/
        ├── __init__.py
        ├── main.py
        ├── config.py
        ├── services/
        │   ├── __init__.py
        │   ├── chat_service.py  # Minimalistic, may be integrated into rag_service initially
        │   ├── gemini_service.py
        │   └── qdrant_service.py
        └── models/
            ├── __init__.py
            └── chat_models.py
```

## 3. Core Modules and Responsibilities

### `backend/src/chatbot_api/main.py`
*   Initialize FastAPI application.
*   Define `POST /chat` endpoint.
    *   Accepts `ChatRequest` (Pydantic model) containing user query.
    *   Calls `rag_service.get_rag_response()`.
    *   Returns `ChatResponse` (Pydantic model).
*   Define `GET /health` endpoint.
*   Configure CORS middleware.

### `backend/src/chatbot_api/config.py`
*   Load environment variables using `python-dotenv`.
*   Define constants for API keys, Qdrant URL, collection name, Gemini models (`gemini-embedding-001`, generative model).
*   Provide a `Settings` class (e.g., using Pydantic's `BaseSettings`) for centralized configuration access.

### `backend/src/chatbot_api/services/gemini_service.py`
*   Initialize Google Generative AI client.
*   `get_embedding(text: str) -> list[float]`: Generates an embedding for the given text using `gemini-embedding-001`. Handles API calls and error conditions.
*   `generate_content(prompt: str) -> str`: Calls the Gemini generative model to produce text based on the provided prompt.

### `backend/src/chatbot_api/services/qdrant_service.py`
*   Initialize Qdrant client connection.
*   `search_documents(query_vector: list[float], top_k: int) -> list[dict]`: Searches the Qdrant collection for `top_k` most similar documents given a query vector.

### `backend/src/chatbot_api/services/rag_service.py`
*   `get_rag_response(query: str) -> str`:
    1.  Call `gemini_service.get_embedding(query)`.
    2.  Call `qdrant_service.search_documents(query_embedding, top_k)`.
    3.  Construct a comprehensive prompt for the Gemini generative model using the original query and the retrieved document content.
    4.  Call `gemini_service.generate_content(final_prompt)`.
    5.  Return the generated response.

### `backend/src/chatbot_api/models/chat_models.py`
*   `ChatRequest(BaseModel)`:
    *   `query: str`
*   `ChatResponse(BaseModel)`:
    *   `response: str`

## 4. Dependencies
*   `fastapi`
*   `uvicorn` (for running the app)
*   `pydantic` (for data validation, often a FastAPI dependency)
*   `python-dotenv`
*   `qdrant-client`
*   `google-generativeai`

## 5. Integration Points
*   **Qdrant Cloud:** Connects via `qdrant-client` using `QDRANT_HOST` and `QDRANT_API_KEY` environment variables.
*   **Gemini API:** Connects via `google-generativeai` using `GEMINI_API_KEY` environment variable. Specific models (`gemini-embedding-001`, generative model) will be configured.
*   **Docusaurus Frontend:** Interacts with the `/chat` and `/health` endpoints via HTTP requests. CORS will be configured on the FastAPI side to allow requests from the Docusaurus origin.

## 6. Error Handling Strategy
*   **API Errors:** Utilize FastAPI's `HTTPException` for standard HTTP error responses (e.g., 400 Bad Request for invalid input, 500 Internal Server Error for unexpected issues).
*   **External Service Errors:** Implement `try-except` blocks around calls to Gemini and Qdrant services to catch their specific exceptions, log them, and translate them into appropriate `HTTPException` responses or internal error messages.
*   **Validation Errors:** Pydantic automatically handles request body validation errors, returning 422 Unprocessable Entity.
*   **Logging:** Use Python's `logging` module to log detailed error messages, stack traces, and relevant context.

## 7. Testing Approach
*   **Unit Tests:**
    *   `test_config.py`: Verify environment variable loading.
    *   `test_gemini_service.py`: Mock Gemini API calls to test embedding generation and content generation.
    *   `test_qdrant_service.py`: Mock Qdrant client calls to test document search.
    *   `test_rag_service.py`: Mock `gemini_service` and `qdrant_service` to test the RAG orchestration logic.
*   **Integration Tests:**
    *   `test_main.py`: Use FastAPI's `TestClient` to make requests to `/chat` and `/health` endpoints, ensuring proper integration of services (can use mocks for external APIs in initial integration tests, then live external APIs for end-to-end).
*   **Fixtures:** Use `pytest` fixtures for setting up test data and mocked clients.

## 8. Deployment Notes
*   The `requirements.txt` will need to be updated with all new dependencies.
*   The `.env` file will need `GEMINI_API_KEY`, `QDRANT_HOST`, `QDRANT_API_KEY`, and `QDRANT_COLLECTION_NAME` variables.
*   Instructions for running the FastAPI app with `uvicorn` will be provided.