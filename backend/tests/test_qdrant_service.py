import pytest
from unittest.mock import MagicMock, patch
import os
from qdrant_client import models
from qdrant_client.http.exceptions import UnexpectedResponse

from backend.src.qdrant_indexer.qdrant_service import QdrantService

@pytest.fixture
def mock_qdrant_client():
    with patch('backend.src.qdrant_indexer.qdrant_service.QdrantClient') as MockClient:
        mock_instance = MockClient.return_value
        yield mock_instance

@pytest.fixture
def qdrant_service(mock_qdrant_client):
    # Mock environment variables for testing
    with patch.dict(os.environ, {
        "QDRANT_HOST": "http://localhost",
        "QDRANT_API_KEY": "test_api_key",
        "QDRANT_COLLECTION_NAME": "test_collection",
        "QDRANT_VECTOR_SIZE": "768"
    }):
        service = QdrantService()
        assert service.client == mock_qdrant_client # Ensure the mock is used
        yield service

def test_qdrant_service_init(mock_qdrant_client):
    with patch.dict(os.environ, {
        "QDRANT_HOST": "http://localhost",
        "QDRANT_API_KEY": "test_api_key",
        "QDRANT_COLLECTION_NAME": "test_collection",
        "QDRANT_VECTOR_SIZE": "768"
    }):
        service = QdrantService()
        mock_qdrant_client.assert_called_once_with(
            host="http://localhost",
            api_key="test_api_key"
        )
        assert service.collection_name == "test_collection"
        assert service.vector_size == 768

def test_recreate_collection(qdrant_service, mock_qdrant_client):
    qdrant_service.recreate_collection()
    mock_qdrant_client.recreate_collection.assert_called_once_with(
        collection_name="test_collection",
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
    )

def test_upsert_points(qdrant_service, mock_qdrant_client):
    points = [
        models.PointStruct(id="1", vector=[0.1]*768, payload={"text": "test1"}),
        models.PointStruct(id="2", vector=[0.2]*768, payload={"text": "test2"})
    ]
    mock_qdrant_client.upsert.return_value = MagicMock(status=models.UpdateStatus.COMPLETED)
    result = qdrant_service.upsert_points(points)
    mock_qdrant_client.upsert.assert_called_once_with(
        collection_name="test_collection",
        wait=True,
        points=points
    )
    assert result.status == models.UpdateStatus.COMPLETED

def test_search(qdrant_service, mock_qdrant_client):
    query_vector = [0.5]*768
    mock_qdrant_client.search.return_value = [MagicMock(id="1", score=0.9)]
    results = qdrant_service.search(query_vector)
    mock_qdrant_client.search.assert_called_once_with(
        collection_name="test_collection",
        query_vector=query_vector,
        query_filter=None,
        limit=5
    )
    assert results[0].id == "1"

def test_get_collection_info(qdrant_service, mock_qdrant_client):
    mock_qdrant_client.get_collection.return_value = MagicMock(config=True)
    info = qdrant_service.get_collection_info()
    mock_qdrant_client.get_collection.assert_called_once_with(collection_name="test_collection")
    assert info.config is True

def test_delete_collection(qdrant_service, mock_qdrant_client):
    qdrant_service.delete_collection()
    mock_qdrant_client.delete_collection.assert_called_once_with(collection_name="test_collection")

def test_get_all_point_ids(qdrant_service, mock_qdrant_client):
    # Mock scroll to simulate pagination
    mock_qdrant_client.scroll.side_effect = [
        ([MagicMock(id="1"), MagicMock(id="2")], "offset_3"),
        ([MagicMock(id="3")], None)
    ]
    ids = qdrant_service.get_all_point_ids()
    assert ids == ["1", "2", "3"]
    assert mock_qdrant_client.scroll.call_count == 2

def test_delete_points(qdrant_service, mock_qdrant_client):
    ids_to_delete = ["1", "2"]
    mock_qdrant_client.delete.return_value = MagicMock(status=models.UpdateStatus.COMPLETED)
    result = qdrant_service.delete_points(ids_to_delete)
    mock_qdrant_client.delete.assert_called_once_with(
        collection_name="test_collection",
        points_selector=models.PointIdsList(points=ids_to_delete),
        wait=True
    )
    assert result.status == models.UpdateStatus.COMPLETED

def test_delete_points_no_ids(qdrant_service, mock_qdrant_client):
    with patch('backend.src.qdrant_indexer.qdrant_service.logger') as mock_logger:
        qdrant_service.delete_points([])
        mock_logger.warning.assert_called_once_with("No points to delete.")
        mock_qdrant_client.delete.assert_not_called()

def test_qdrant_service_init_missing_env():
    with patch.dict(os.environ, {}, clear=True): # Clear env for this test
        with pytest.raises(ValueError, match="QDRANT_HOST or QDRANT_API_KEY not found in environment variables."):
            QdrantService()
