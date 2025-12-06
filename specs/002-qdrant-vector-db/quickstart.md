# Quickstart: Qdrant Indexing Script

**Purpose**: This guide provides instructions on how to set up the environment and run the Python script to index Docusaurus book content into Qdrant Cloud.

## Prerequisites

- **Python**: Version 3.9 or higher.
- **pip**: Python package installer (comes with Python).
- **Qdrant Cloud Account**: With a created collection or the ability to create one via API.
- **Qdrant API Key and URL**: Obtain these from your Qdrant Cloud dashboard.
- **Google Gemini API Key**: For generating embeddings.

## Setup & Installation

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:
    This command will install all required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory with your Qdrant and Gemini API credentials:
    ```dotenv
    QDRANT_HOST="your_qdrant_cloud_url"
    QDRANT_API_KEY="your_qdrant_api_key"
    GEMINI_API_KEY="your_google_gemini_api_key"
    QDRANT_COLLECTION_NAME="docusaurus-book-content" # Or your preferred name
    ```

## Running the Indexing Script

1.  **Ensure virtual environment is active** (see step 3 above).

2.  **Execute the indexing script**:
    The script will parse your Docusaurus Markdown files, generate embeddings, and upload them to Qdrant.
    ```bash
    python src/qdrant_indexer/main.py --action index --docs-path ../book-site/docs
    ```
    *   `--action index`: Specifies the indexing action.
    *   `--docs-path`: Path to your Docusaurus `docs` directory.

## Re-indexing Content

To update or add new content to Qdrant, simply run the indexing script again. The script will handle upserting new/modified data.

```bash
python src/qdrant_indexer/main.py --action index --docs-path ../book-site/docs
```
