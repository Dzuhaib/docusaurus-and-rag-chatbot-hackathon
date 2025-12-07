import pytest
from unittest.mock import patch, MagicMock
from backend.src.chatbot_api.services import rag_service
from backend.src.chatbot_api.services import gemini_service
from backend.src.chatbot_api.services import qdrant_service

@pytest.fixture
def mock_gemini_service():
    with patch('backend.src.chatbot_api.services.gemini_service.get_embedding') as mock_embed, \
         patch('backend.src.chatbot_api.services.gemini_service.generate_content') as mock_generate:
        yield mock_embed, mock_generate

@pytest.fixture
def mock_qdrant_service():
    with patch('backend.src.chatbot_api.services.qdrant_service.search_documents') as mock:
        yield mock

def test_get_rag_response_success(mock_gemini_service, mock_qdrant_service):
    mock_embed, mock_generate = mock_gemini_service
    
    # Mock return values
    mock_embed.return_value = [0.1, 0.2, 0.3]
    mock_qdrant_service.return_value = [
        {"text": "Contextual document one."},
        {"text": "Contextual document two."}
    ]
    mock_generate.return_value = "This is a generated answer based on context."

    query = "What is the capital of France?"
    response = rag_service.get_rag_response(query)

    mock_embed.assert_called_once_with(query)
    mock_qdrant_service.assert_called_once_with([0.1, 0.2, 0.3], 3)
    
    expected_prompt_substring_1 = "Contextual document one."
    expected_prompt_substring_2 = "Contextual document two."
    expected_prompt_substring_3 = "Question: What is the capital of France?"

    # Check if the prompt passed to generate_content contains parts of context and query
    assert mock_generate.call_args[0][0] is not None
    assert expected_prompt_substring_1 in mock_generate.call_args[0][0]
    assert expected_prompt_substring_2 in mock_generate.call_args[0][0]
    assert expected_prompt_substring_3 in mock_generate.call_args[0][0]

    assert response == "This is a generated answer based on context."

def test_get_rag_response_no_documents(mock_gemini_service, mock_qdrant_service):
    mock_embed, mock_generate = mock_gemini_service
    
    mock_embed.return_value = [0.1, 0.2, 0.3]
    mock_qdrant_service.return_value = [] # No documents found
    mock_generate.return_value = "I don't have specific information, but I can try to answer."

    query = "How does a black hole work?"
    response = rag_service.get_rag_response(query)

    mock_embed.assert_called_once_with(query)
    mock_qdrant_service.assert_called_once_with([0.1, 0.2, 0.3], 3)
    
    # Check if the prompt is built without context
    assert "Context:" not in mock_generate.call_args[0][0]
    assert "Question: How does a black hole work?" in mock_generate.call_args[0][0]

    assert response == "I don't have specific information, but I can try to answer."

def test_get_rag_response_embedding_failure(mock_gemini_service, mock_qdrant_service):
    mock_embed, _ = mock_gemini_service
    
    mock_embed.return_value = None # Simulate embedding failure
    
    query = "What is the weather?"
    response = rag_service.get_rag_response(query)

    mock_embed.assert_called_once_with(query)
    mock_qdrant_service.assert_not_called() # Qdrant search should not be called
    assert response == "Could not generate embedding for your query."

def test_get_rag_response_generative_failure(mock_gemini_service, mock_qdrant_service):
    mock_embed, mock_generate = mock_gemini_service
    
    mock_embed.return_value = [0.1, 0.2, 0.3]
    mock_qdrant_service.return_value = [{"text": "Context for generation."}]
    mock_generate.side_effect = Exception("Generative Model Error")

    query = "Tell me a story."
    response = rag_service.get_rag_response(query)

    mock_embed.assert_called_once_with(query)
    mock_qdrant_service.assert_called_once_with([0.1, 0.2, 0.3], 3)
    assert "An error occurred while processing your request." in response
