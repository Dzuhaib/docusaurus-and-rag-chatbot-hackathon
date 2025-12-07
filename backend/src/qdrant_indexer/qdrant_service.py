import os
import logging
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
from typing import List

load_dotenv()

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_HOST"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "docusaurus_book_content")
        # Vector size for Google Gemini Embeddings - need to confirm this
        # Assuming a common size, will be adjusted if needed after integrating embedding model
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", 3072)) # Vector size for gemini-embedding-001 (actual observed)

    def recreate_collection(self):
        logger.info(f"Recreating collection: {self.collection_name}")
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
        )
        logger.info(f"Collection {self.collection_name} recreated successfully.")

    def upsert_points(self, points, batch_size=16):
        """
        Upserts (updates or inserts) points into the Qdrant collection in batches.
        :param points: List of models.PointStruct objects.
        :param batch_size: The number of points to upsert in a single batch.
        """
        if not points:
            logger.warning("No points to upsert.")
            return

        logger.info(f"Upserting {len(points)} points into collection {self.collection_name} in batches of {batch_size}...")
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            try:
                operation_info = self.client.upsert(
                    collection_name=self.collection_name,
                    wait=True,
                    points=batch
                )
                logger.info(f"Upserted batch {i//batch_size + 1}/{(len(points) + batch_size - 1)//batch_size}. Status: {operation_info.status}")
            except Exception as e:
                logger.error(f"Failed to upsert batch {i//batch_size + 1}: {e}")
                raise
        
        logger.info("All batches upserted successfully.")

    def search(self, query_vector, limit=5, query_filter=None):
        """
        Performs a semantic search on the Qdrant collection.
        """
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit
        )
        return search_result

    def get_collection_info(self):
        return self.client.get_collection(collection_name=self.collection_name)

    def delete_collection(self):
        logger.info(f"Deleting collection: {self.collection_name}")
        self.client.delete_collection(collection_name=self.collection_name)
        logger.info(f"Collection {self.collection_name} deleted successfully.")

    def get_all_point_ids(self) -> List[str]:
        """Fetches all point IDs from the collection."""
        all_ids = []
        offset = None
        while True:
            scroll_result, next_page_offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100, # Fetch in batches
                offset=offset,
                with_vectors=False,
                with_payload=False
            )
            all_ids.extend([point.id for point in scroll_result])
            if next_page_offset is None:
                break
            offset = next_page_offset
        return [str(uid) for uid in all_ids] # Convert UUIDs to strings

    def delete_points(self, ids: List[str]):
        """Deletes points from the collection by their IDs."""
        if not ids:
            logger.warning("No points to delete.")
            return

        logger.info(f"Deleting {len(ids)} points from collection {self.collection_name}...")
        operation_info = self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=ids),
            wait=True
        )
        logger.info(f"Delete operation finished with status: {operation_info.status}")
        return operation_info
