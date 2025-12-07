import pytest
from unittest.mock import patch, MagicMock
from backend.src.chatbot_api.services import gemini_service
from backend.src.chatbot_api.config import settings

@pytest.fixture
def mock_genai_configure():
    with patch('google.generativeai.configure') as mock:
        yield mock

@pytest.fixture
def mock_embed_content():
    with patch('google.generativeai.embed_content') as mock:
        yield mock

@pytest.fixture
def mock_generative_model():
    with patch('google.generativeai.GenerativeModel') as mock:
        yield mock

def test_get_embedding_success(mock_embed_content, mock_genai_configure):
    mock_embed_content.return_value = {'embedding': [0.1, 0.2, 0.3]}
    text_to_embed = "test text"
    embedding = gemini_service.get_embedding(text_to_embed)

    mock_genai_configure.assert_called_once_with(api_key=settings.GEMINI_API_KEY)
    mock_embed_content.assert_called_once_with(
        model=settings.EMBEDDING_MODEL,
        content=text_to_embed
    )
    assert embedding == [0.1, 0.2, 0.3]

def test_get_embedding_api_error(mock_embed_content, mock_genai_configure):
    mock_embed_content.side_effect = Exception("API Error")
    text_to_embed = "test text"

    with pytest.raises(Exception, match="API Error"):
        gemini_service.get_embedding(text_to_embed)

    mock_genai_configure.assert_called_once_with(api_key=settings.GEMINI_API_KEY)
    mock_embed_content.assert_called_once_with(
        model=settings.EMBEDDING_MODEL,
        content=text_to_embed
    )

def test_generate_content_success(mock_generative_model, mock_genai_configure):
    mock_response = MagicMock()
    mock_response.text = "Generated response"
    mock_generative_model.return_value.generate_content.return_value = mock_response

    prompt = "Generate a response"
    response = gemini_service.generate_content(prompt)

    mock_genai_configure.assert_called_once_with(api_key=settings.GEMINI_API_KEY)
    mock_generative_model.assert_called_once_with(model_name=settings.GENERATIVE_MODEL)
    mock_generative_model.return_value.generate_content.assert_called_once_with(prompt)
    assert response == "Generated response"

def test_generate_content_api_error(mock_generative_model, mock_genai_configure):
    mock_generative_model.return_value.generate_content.side_effect = Exception("Generation Error")
    prompt = "Generate a response"

    with pytest.raises(Exception, match="Generation Error"):
        gemini_service.generate_content(prompt)

    mock_genai_configure.assert_called_once_with(api_key=settings.GEMINI_API_KEY)
    mock_generative_model.assert_called_once_with(model_name=settings.GENERATIVE_MODEL)
    mock_generative_model.return_value.generate_content.assert_called_once_with(prompt)
