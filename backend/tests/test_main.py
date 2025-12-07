import pytest
from unittest.mock import patch, MagicMock
import os
import typer
from typer.testing import CliRunner

from backend.src.qdrant_indexer.main import app
from backend.src.qdrant_indexer.qdrant_service import QdrantService
from backend.src.qdrant_indexer.text_processor import TextProcessor

runner = CliRunner()

@pytest.fixture
def mock_services():
    with patch('backend.src.qdrant_indexer.main.QdrantService') as MockQdrantService, \
         patch('backend.src.qdrant_indexer.main.TextProcessor') as MockTextProcessor, \
         patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_gemini_key", "QDRANT_HOST": "dummy_host"}):
        
        mock_qdrant_instance = MockQdrantService.return_value
        mock_text_processor_instance = MockTextProcessor.return_value

        # Mock QdrantService methods
        mock_qdrant_instance.get_collection_info.side_effect = Exception("Collection not found")
        mock_qdrant_instance.recreate_collection.return_value = None
        mock_qdrant_instance.upsert_points.return_value = MagicMock(status=models.UpdateStatus.COMPLETED)
        mock_qdrant_instance.get_all_point_ids.return_value = ["old_id_1", "old_id_2"]
        mock_qdrant_instance.delete_points.return_value = None

        # Mock TextProcessor methods
        mock_text_processor_instance.load_all_markdown_content.return_value = [
            {"text": "chunk1", "chunk_id": "new_id_1"},
            {"text": "chunk2", "chunk_id": "new_id_3"}
        ]
        mock_text_processor_instance.get_embeddings.return_value = [[0.1]*768, [0.2]*768]

        yield mock_qdrant_instance, mock_text_processor_instance

def test_index_command_recreate(mock_services):
    mock_qdrant_instance, mock_text_processor_instance = mock_services
    
    result = runner.invoke(app, ["index", "--recreate", "--docs-path", "dummy_path"])
    
    assert result.exit_code == 0
    mock_qdrant_instance.recreate_collection.assert_called_once()
    mock_text_processor_instance.load_all_markdown_content.assert_called_once()
    mock_text_processor_instance.get_embeddings.assert_called_once()
    mock_qdrant_instance.upsert_points.assert_called_once()
    assert "Indexing process completed successfully." in result.stdout

def test_index_command_existing_collection(mock_services):
    mock_qdrant_instance, mock_text_processor_instance = mock_services
    mock_qdrant_instance.get_collection_info.side_effect = None # Collection exists
    
    result = runner.invoke(app, ["index", "--docs-path", "dummy_path"])
    
    assert result.exit_code == 0
    mock_qdrant_instance.get_collection_info.assert_called_once()
    mock_qdrant_instance.recreate_collection.assert_not_called() # Should not recreate
    assert "Collection 'test_collection' already exists." in result.stdout

def test_index_command_new_collection(mock_services):
    mock_qdrant_instance, mock_text_processor_instance = mock_services
    mock_qdrant_instance.get_collection_info.side_effect = Exception("Collection not found") # Simulate no collection
    
    result = runner.invoke(app, ["index", "--docs-path", "dummy_path"])
    
    assert result.exit_code == 0
    mock_qdrant_instance.get_collection_info.assert_called_once()
    mock_qdrant_instance.recreate_collection.assert_called_once() # Should recreate
    assert "Collection 'test_collection' does not exist. Creating it." in result.stdout

def test_index_command_no_content(mock_services):
    mock_qdrant_instance, mock_text_processor_instance = mock_services
    mock_text_processor_instance.load_all_markdown_content.return_value = []
    
    result = runner.invoke(app, ["index", "--docs-path", "dummy_path"])
    
    assert result.exit_code == 0
    assert "No content found to index. Exiting." in result.stdout
    mock_qdrant_instance.upsert_points.assert_not_called()

def test_index_command_deletes_stale_points(mock_services):
    mock_qdrant_instance, mock_text_processor_instance = mock_services
    mock_qdrant_instance.get_collection_info.side_effect = None # Collection exists
    mock_qdrant_instance.get_all_point_ids.return_value = ["old_id_1", "old_id_2", "old_id_3"] # Simulate existing points
    mock_text_processor_instance.load_all_markdown_content.return_value = [
        {"text": "chunk1", "chunk_id": "old_id_1"},
        {"text": "chunk2", "chunk_id": "new_id_4"} # old_id_2 and old_id_3 are stale
    ]
    
    result = runner.invoke(app, ["index", "--docs-path", "dummy_path"])
    
    assert result.exit_code == 0
    mock_qdrant_instance.get_all_point_ids.assert_called_once()
    mock_qdrant_instance.delete_points.assert_called_once_with(
        ["old_id_2", "old_id_3"] # Assuming order
    )
    assert "Identified 2 stale points to delete from Qdrant." in result.stdout
