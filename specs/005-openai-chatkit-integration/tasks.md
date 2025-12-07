---
id: 05
title: Tasks for FastAPI Backend with Chatkit and Gemini Embeddings
stage: tasks
date: 2025-12-06
model: Gemini 1.5 Flash
feature: openai-chatkit-integration
branch: main
user: current_user
command: "create tasks for FastAPI Chatkit Backend using gemini-embedding-001"
labels: ["backend", "fastapi", "chatkit", "gemini", "qdrant", "tasks", "rag"]
links:
  spec: specs/005-openai-chatkit-integration/spec.md
  plan: specs/005-openai-chatkit-integration/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/005-openai-chatkit-integration/tasks.md
tests_yaml: []
prompt_text: "Let's do Backend: FastAPI (using Chatkit.js and Chatkit.py, though this was later refined/questioned regarding its role with OpenAI). create constitution first, specify then, plan, tasks. and use gemini-embedding-001 instead of embedding-001"
response_text: "Tasks created for the FastAPI Backend with Chatkit integration and gemini-embedding-001."
outcome: "Tasks created successfully."
evaluation: "The tasks provide a granular breakdown of the implementation steps, including file modifications and new file creations, to guide the development process."
---
# Tasks for FastAPI Backend with Chatkit and Gemini Embeddings

This document outlines the detailed tasks required to implement the FastAPI backend for the RAG chatbot, integrating Chatkit, Gemini embeddings, and Qdrant.

## Task 1: Project Setup and Dependency Installation
*   **Objective:** Create the `chatbot_api` directory structure and install necessary Python dependencies.
*   **Files Modified:**
    *   `backend/requirements.txt`
*   **Files Created:**
    *   `backend/src/chatbot_api/__init__.py`
    *   `backend/src/chatbot_api/services/__init__.py`
    *   `backend/src/chatbot_api/models/__init__.py`
*   **Steps:**
    1.  Create the directory `backend/src/chatbot_api`.
    2.  Create subdirectories `services` and `models` inside `chatbot_api`.
    3.  Create empty `__init__.py` files in `chatbot_api`, `services`, and `models`.
    4.  Add `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`, `qdrant-client`, `google-generativeai` to `backend/requirements.txt`.
    5.  Run `pip install -r backend/requirements.txt`.

## Task 2: Configuration Module (`config.py`)
*   **Objective:** Create a module to handle environment variables and application settings.
*   **Files Created:**
    *   `backend/src/chatbot_api/config.py`
*   **Steps:**
    1.  Create `config.py` in `backend/src/chatbot_api/`.
    2.  Implement a `Settings` class (e.g., using `pydantic_settings.BaseSettings` for robust type-hinted settings) that loads:
        *   `GEMINI_API_KEY`
        *   `QDRANT_HOST`
        *   `QDRANT_API_KEY`
        *   `QDRANT_COLLECTION_NAME`
        *   `EMBEDDING_MODEL` (e.g., `gemini-embedding-001`)
        *   `GENERATIVE_MODEL` (e.g., `gemini-pro`)
    3.  Ensure `.env` file loading is handled (e.g., `load_dotenv()`).

## Task 3: Pydantic Models (`chat_models.py`)
*   **Objective:** Define request and response models for the chat API.
*   **Files Created:**
    *   `backend/src/chatbot_api/models/chat_models.py`
*   **Steps:**
    1.  Create `chat_models.py` in `backend/src/chatbot_api/models/`.
    2.  Define `ChatRequest` model with `query: str`.
    3.  Define `ChatResponse` model with `response: str`.

## Task 4: Gemini Service (`gemini_service.py`)
*   **Objective:** Implement functions to interact with the Google Gemini API for embeddings and content generation.
*   **Files Created:**
    *   `backend/src/chatbot_api/services/gemini_service.py`
*   **Steps:**
    1.  Create `gemini_service.py` in `backend/src/chatbot_api/services/`.
    2.  Import `google.generativeai`.
    3.  Implement `get_embedding(text: str) -> list[float]` using `genai.embed_content` with `model=settings.EMBEDDING_MODEL`.
    4.  Implement `generate_content(prompt: str) -> str` using `genai.GenerativeModel(settings.GENERATIVE_MODEL).generate_content`.
    5.  Include error handling for API calls.

## Task 5: Qdrant Service (`qdrant_service.py`)
*   **Objective:** Implement functions to interact with the Qdrant vector database.
*   **Files Created:**
    *   `backend/src/chatbot_api/services/qdrant_service.py`
*   **Steps:**
    1.  Create `qdrant_service.py` in `backend/src/chatbot_api/services/`.
    2.  Import `QdrantClient`.
    3.  Initialize `QdrantClient` with `settings.QDRANT_HOST` and `settings.QDRANT_API_KEY`.
    4.  Implement `search_documents(query_vector: list[float], top_k: int) -> list[dict]`. This function should query `settings.QDRANT_COLLECTION_NAME` and return relevant document payloads.

## Task 6: RAG Service (`rag_service.py`)
*   **Objective:** Orchestrate the RAG process using Gemini and Qdrant services.
*   **Files Created:**
    *   `backend/src/chatbot_api/services/rag_service.py`
*   **Steps:**
    1.  Create `rag_service.py` in `backend/src/chatbot_api/services/`.
    2.  Import `gemini_service` and `qdrant_service`.
    3.  Implement `get_rag_response(query: str, top_k: int = 3) -> str`.
        *   Get embedding for `query`.
        *   Search Qdrant for top `top_k` documents.
        *   Construct an informative prompt for the generative model, including the original query and the content from retrieved documents.
        *   Call `gemini_service.generate_content` with the constructed prompt.
        *   Return the generated response.

## Task 7: Main FastAPI Application (`main.py`)
*   **Objective:** Set up the FastAPI application, define API routes, and configure CORS.
*   **Files Created:**
    *   `backend/src/chatbot_api/main.py`
*   **Steps:**
    1.  Create `main.py` in `backend/src/chatbot_api/`.
    2.  Initialize FastAPI app.
    3.  Implement `GET /health` endpoint.
    4.  Implement `POST /chat` endpoint:
        *   Accepts `ChatRequest`.
        *   Calls `rag_service.get_rag_response`.
        *   Returns `ChatResponse`.
    5.  Add CORS middleware to allow requests from the Docusaurus frontend.

## Task 8: Update Backend `__init__.py` to Expose API
*   **Objective:** Make the FastAPI app discoverable or importable from the main backend entry point if needed.
*   **Files Modified:**
    *   `backend/src/qdrant_indexer/api.py` (This might be the existing `api.py` if the intent is to integrate, or a new `api.py` in `chatbot_api` if it's standalone). *Correction: Based on the folder structure and previous work, `qdrant_indexer` contains the old API. A new `api.py` in `chatbot_api` makes more sense to contain the new FastAPI app.*
    *   Consider `backend/src/qdrant_indexer/main.py` for entry point.
*   **Steps:**
    1.  Ensure `backend/src/chatbot_api/main.py` is the entry point for running the chatbot API. No direct modification to `qdrant_indexer/api.py` is needed if `chatbot_api` is standalone.

## Task 9: Basic Testing
*   **Objective:** Create initial test files for core services and the main API endpoint.
*   **Files Created:**
    *   `backend/tests/test_chatbot_api_config.py`
    *   `backend/tests/test_chatbot_api_gemini_service.py`
    *   `backend/tests/test_chatbot_api_qdrant_service.py`
    *   `backend/tests/test_chatbot_api_rag_service.py`
    *   `backend/tests/test_chatbot_api_main.py`
*   **Steps:**
    1.  Create basic test files in `backend/tests/`.
    2.  Implement simple unit tests for configuration loading, Gemini service (mocked), Qdrant service (mocked), RAG service (mocked).
    3.  Implement an integration test for the `/health` endpoint and a basic (mocked external calls) test for the `/chat` endpoint.

## Task 10: Environment Variable File
*   **Objective:** Provide a template for the `.env` file.
*   **Files Created:**
    *   `backend/.env.example`
*   **Steps:**
    1.  Create `backend/.env.example` with placeholders for `GEMINI_API_KEY`, `QDRANT_HOST`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`, `EMBEDDING_MODEL`, `GENERATIVE_MODEL`.

## Task 11: Instructions for Running
*   **Objective:** Provide clear instructions for the user to run the FastAPI backend.
*   **Files Modified:**
    *   `README.md` (or similar project-level documentation, if available)
*   **Steps:**
    1.  Add instructions to `backend/README.md` (if it exists, otherwise create it) on how to:
        *   Set up the `.env` file.
        *   Install dependencies.
        *   Run the FastAPI application using `uvicorn`.