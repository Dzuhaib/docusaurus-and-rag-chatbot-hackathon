# FastAPI RAG Chatbot Backend

This directory contains the FastAPI backend application for the Retrieval Augmented Generation (RAG) chatbot, leveraging Google's Gemini API for embeddings and content generation, and Qdrant Cloud for vector search.

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the `backend/` directory based on the provided `.env.example`. Replace the placeholder values with your actual API keys and host information:

```
# .env.example content:
# Google Gemini API Key
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

# Qdrant Cloud Cluster URL and API Key
QDRANT_HOST="YOUR_QDRANT_CLUSTER_URL_HERE"
QDRANT_API_KEY="YOUR_QDRANT_API_KEY_HERE"
QDRANT_COLLECTION_NAME="book_rag" # Or your specific collection name

# Gemini Models to Use
EMBEDDING_MODEL="gemini-embedding-001"
GENERATIVE_MODEL="gemini-pro"
```

**Important:** Never commit your `.env` file to version control.

### 2. Install Dependencies

Navigate to the `backend/` directory in your terminal and install the required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the FastAPI Application

Once dependencies are installed and your `.env` file is configured, you can run the FastAPI application using `uvicorn`. Ensure you are in the project root directory (C:\specify\new_session8) or the `backend` directory when running this command, depending on how your Python environment is set up to find the `backend.src.chatbot_api.main` module.

If running from the project root (C:\specify\new_session8):
```bash
uvicorn backend.src.chatbot_api.main:app --host 0.0.0.0 --port 8000 --reload
```

If running from the `backend/` directory:
```bash
cd backend
uvicorn src.chatbot_api.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag is useful during development for automatic code reloading on changes. The API will be accessible at `http://localhost:8000`.

## API Endpoints

*   **GET `/health`**: Checks the health of the API. Returns `{"status": "ok"}`.
*   **POST `/chat`**: Sends a query to the RAG chatbot and receives a response.
    *   **Request Body**: `{"query": "Your question here."}`
    *   **Response Body**: `{"response": "The chatbot's answer here."}`

## Testing

To run the tests for the chatbot API, navigate to the `backend/` directory and execute `pytest`:

```bash
cd backend
pytest tests/
```
