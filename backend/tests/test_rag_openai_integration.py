import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from chatbot_api.main import app
from chatbot_api.config import settings

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict('os.environ', {
        'GENERATIVE_MODEL_PROVIDER': 'openai',
        'OPENAI_API_KEY': 'test_openai_key',
        'OPENAI_EMBEDDING_MODEL': 'test_embedding_model',
        'OPENAI_CHAT_MODEL': 'test_chat_model',
        'QDRANT_HOST': 'test_qdrant_host',
        'QDRANT_API_KEY': 'test_qdrant_api_key',
        'QDRANT_COLLECTION_NAME': 'test_collection'
    }):
        # Reload settings to pick up mocked env vars
        from chatbot_api import config
        # This forces the settings to reload from os.environ
        config.settings = config.Settings() 
        yield
        # Reset settings after test if necessary, though reloading above should handle it.

@patch('chatbot_api.services.qdrant_service.search_documents')
@patch('chatbot_api.services.rag_service.openai_service_instance')
def test_rag_openai_integration_success(mock_openai_service_instance, mock_search_documents):
    # Mock Qdrant search results
    mock_search_documents.return_value = [
        {"id": "1", "text": "Contextual document one."},
        {"id": "2", "text": "Contextual document two."}
    ]

    # Mock OpenAI embedding response
    mock_openai_service_instance.get_embedding.return_value = [0.1, 0.2, 0.3]

    # Mock OpenAI chat completion response
    mock_openai_service_instance.generate_content.return_value = "Integrated OpenAI response based on context."

    request_payload = {"query": "Tell me about the book."}
    response = client.post("/chat", json=request_payload)

    assert response.status_code == 200
    assert response.json() == {"response": "Integrated OpenAI response based on context."}

    # Verify that OpenAI embedding was called
    mock_openai_service_instance.get_embedding.assert_called_once()
    # Verify that Qdrant search was called
    mock_search_documents.assert_called_once()
    # Verify that OpenAI chat completion was called
    mock_openai_service_instance.generate_content.assert_called_once()
