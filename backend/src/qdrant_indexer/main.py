import typer
import os
import logging
from typing import Optional
from qdrant_client import models
from dotenv import load_dotenv

from .qdrant_service import QdrantService
from .text_processor import TextProcessor
from .rag_service import RAGService

# Load environment variables from .env file
load_dotenv()

app = typer.Typer()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.command()
def index(
    docs_path: str = typer.Option(
        os.path.join("..", "book-site", "docs"),
        "--docs-path",
        "-d",
        help="Path to the Docusaurus docs directory containing Markdown files.",
    ),
    collection_name: Optional[str] = typer.Option(
        None, "--collection-name", "-c", help="Name of the Qdrant collection."
    ),
    recreate: bool = typer.Option(
        False, "--recreate", "-r", help="Recreate the Qdrant collection if it already exists."
    )
):
    """
    Indexes the Docusaurus book content into a Qdrant vector database.
    """
    logger.info(f"Starting indexing process for docs path: {docs_path}")

    # Initialize Qdrant Service
    qdrant_service = QdrantService()
    if collection_name:
        qdrant_service.collection_name = collection_name
    
    # Ensure collection exists
    try:
        if recreate:
            qdrant_service.recreate_collection()
        else:
            try:
                qdrant_service.get_collection_info()
                logger.info(f"Collection '{qdrant_service.collection_name}' already exists.")
            except Exception: # Collection does not exist
                logger.info(f"Collection '{qdrant_service.collection_name}' does not exist. Creating it.")
                qdrant_service.recreate_collection()
    except Exception as e:
        logger.error(f"Failed to ensure Qdrant collection: {e}")
        raise typer.Exit(code=1)

    # Initialize Text Processor
    text_processor = TextProcessor(docs_base_path=docs_path)

    # Load and process all Markdown content
    logger.info("Loading and processing Markdown content...")
    all_processed_chunks = text_processor.load_all_markdown_content()
    logger.info(f"Processed {len(all_processed_chunks)} text chunks.")

    if not all_processed_chunks:
        logger.warning("No content found to index. Exiting.")
        raise typer.Exit(code=0)

    # Prepare for embedding and upsert
    points = []
    texts_to_embed = [chunk["text"] for chunk in all_processed_chunks]

    logger.info(f"Generating embeddings for {len(texts_to_embed)} text chunks using Google Gemini...")
    try:
        embeddings = text_processor.get_embeddings(texts_to_embed, task_type="retrieval_document")
        if len(embeddings) != len(texts_to_embed):
            logger.error("Mismatch between number of texts and generated embeddings.")
            raise ValueError("Embedding generation failed partially.")
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        raise typer.Exit(code=1)

    for i, chunk_data in enumerate(all_processed_chunks):
        points.append(
            models.PointStruct(
                id=chunk_data["chunk_id"],
                vector=embeddings[i],
                payload=chunk_data
            )
        )
    
    # Upsert points to Qdrant
    try:
        # Get existing point IDs before upserting new ones
        existing_qdrant_ids = set(qdrant_service.get_all_point_ids())
        logger.info(f"Found {len(existing_qdrant_ids)} existing points in Qdrant.")

        qdrant_service.upsert_points(points)
        logger.info("Indexing process completed successfully.")

        # Identify and delete stale points
        current_processed_ids = {point.id for point in points}
        stale_ids = list(existing_qdrant_ids - current_processed_ids)

        if stale_ids:
            logger.info(f"Identified {len(stale_ids)} stale points to delete from Qdrant.")
            qdrant_service.delete_points(stale_ids)
        else:
            logger.info("No stale points identified for deletion.")

    except Exception as e:
        logger.error(f"Failed to upsert or delete points in Qdrant: {e}")
        raise typer.Exit(code=1)

@app.command()
def query_rag(
    query: str = typer.Argument(..., help="The query to send to the RAG system."),
    docs_path: str = typer.Option(
        os.path.join("..", "book-site", "docs"),
        "--docs-path",
        "-d",
        help="Path to the Docusaurus docs directory containing Markdown files (used for TextProcessor init).",
    ),
    collection_name: Optional[str] = typer.Option(
        None, "--collection-name", "-c", help="Name of the Qdrant collection to query."
    ),
    top_k: int = typer.Option(
        5, "--top-k", "-k", help="Number of top relevant documents to retrieve from Qdrant."
    )
):
    """
    Queries the RAG system with a given question and returns an answer.
    """
    logger.info(f"Processing RAG query: '{query}'")

    qdrant_service = QdrantService()
    if collection_name:
        qdrant_service.collection_name = collection_name
    
    text_processor = TextProcessor(docs_base_path=docs_path)
    rag_service = RAGService(qdrant_service=qdrant_service, text_processor=text_processor)

    answer = rag_service.query_rag(query=query, top_k=top_k)
    print(f"\nAnswer:\n{answer}")
    logger.info("RAG query processing completed.")

if __name__ == "__main__":
    app()