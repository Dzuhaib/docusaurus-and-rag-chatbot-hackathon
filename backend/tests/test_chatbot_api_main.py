import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.src.chatbot_api.main import app
from backend.src.chatbot_api.models.chat_models import ChatRequest, ChatResponse

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch('backend.src.chatbot_api.services.rag_service.get_rag_response')
def test_chat_endpoint_success(mock_get_rag_response):
    mock_get_rag_response.return_value = "Mocked RAG response."
    
    request_payload = {"query": "Hello, bot!"}
    response = client.post("/chat", json=request_payload)
    
    assert response.status_code == 200
    assert response.json() == {"response": "Mocked RAG response."}
    mock_get_rag_response.assert_called_once_with("Hello, bot!")

@patch('backend.src.chatbot_api.services.rag_service.get_rag_response')
def test_chat_endpoint_rag_failure(mock_get_rag_response):
    mock_get_rag_response.side_effect = Exception("RAG service failed.")
    
    request_payload = {"query": "Something went wrong."}
    response = client.post("/chat", json=request_payload)
    
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"]
    mock_get_rag_response.assert_called_once_with("Something went wrong.")

def test_chat_endpoint_invalid_input():
    request_payload = {"invalid_field": "some_value"}
    response = client.post("/chat", json=request_payload)
    
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error
    assert "field required" in response.json()["detail"][0]["msg"]
