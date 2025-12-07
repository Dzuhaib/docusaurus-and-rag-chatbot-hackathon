from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue # Removed Query, NamedVector, TextQuery
from ..config import settings
from typing import List, Dict, Optional

client = QdrantClient(url=settings.QDRANT_HOST, api_key=settings.QDRANT_API_KEY)

def search_documents(query_vector: List[float], top_k: int = 3) -> List[Dict]: # Removed query_text parameter
    """
    Searches the Qdrant collection for the top_k most similar documents to the query vector.
    Returns a list of dictionaries, where each dictionary represents a document's payload.
    """
    try:
        # Revert to purely vector-based search
        search_result = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_vector, # Pass query_vector directly
            limit=top_k,
            with_payload=True
        )
        points = search_result.points
        return [hit.payload for hit in points]
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return []
