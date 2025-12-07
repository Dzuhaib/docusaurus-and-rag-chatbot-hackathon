import pytest
from unittest.mock import patch, MagicMock
from backend.src.chatbot_api.services import qdrant_service
from backend.src.chatbot_api.config import settings
from qdrant_client.models import ScoredPoint

@pytest.fixture
def mock_qdrant_client():
    with patch('backend.src.chatbot_api.services.qdrant_service.QdrantClient') as mock:
        yield mock.return_value

def test_search_documents_success(mock_qdrant_client):
    mock_point = MagicMock(spec=ScoredPoint)
    mock_point.payload = {"text": "document 1 content"}
    mock_qdrant_client.search.return_value = [mock_point]

    query_vector = [0.1, 0.2, 0.3]
    top_k = 1
    result = qdrant_service.search_documents(query_vector, top_k)

    mock_qdrant_client.search.assert_called_once_with(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    assert result == [{"text": "document 1 content"}]

def test_search_documents_multiple_results(mock_qdrant_client):
    mock_point1 = MagicMock(spec=ScoredPoint)
    mock_point1.payload = {"text": "document 1 content"}
    mock_point2 = MagicMock(spec=ScoredPoint)
    mock_point2.payload = {"text": "document 2 content"}
    mock_qdrant_client.search.return_value = [mock_point1, mock_point2]

    query_vector = [0.1, 0.2, 0.3]
    top_k = 2
    result = qdrant_service.search_documents(query_vector, top_k)

    mock_qdrant_client.search.assert_called_once_with(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    assert result == [{"text": "document 1 content"}, {"text": "document 2 content"}]

def test_search_documents_no_results(mock_qdrant_client):
    mock_qdrant_client.search.return_value = []

    query_vector = [0.1, 0.2, 0.3]
    top_k = 1
    result = qdrant_service.search_documents(query_vector, top_k)

    mock_qdrant_client.search.assert_called_once_with(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    assert result == []

def test_search_documents_api_error(mock_qdrant_client):
    mock_qdrant_client.search.side_effect = Exception("Qdrant API Error")

    query_vector = [0.1, 0.2, 0.3]
    top_k = 1
    result = qdrant_service.search_documents(query_vector, top_k)

    mock_qdrant_client.search.assert_called_once_with(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    assert result == [] # Error handling in service returns empty list
