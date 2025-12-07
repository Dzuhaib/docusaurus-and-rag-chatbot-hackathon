import pytest
from unittest.mock import MagicMock, patch
from chatbot_api.services.openai_service import OpenAIService
from chatbot_api.config import settings

@pytest.fixture
def mock_openai_client(mocker):
    # Patch the OpenAI class where it's imported in openai_service.py
    mock_openai = mocker.patch('chatbot_api.services.openai_service.OpenAI')
    yield mock_openai

@pytest.fixture
def openai_service_instance(mock_openai_client):
    # We want to ensure that each test gets a fresh instance
    # and that environment variables are potentially mocked if needed
    with patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test_api_key',
        'OPENAI_EMBEDDING_MODEL': 'text-embedding-ada-002',
        'OPENAI_CHAT_MODEL': 'gpt-3.5-turbo'
    }):
        # OpenAIService will now use the mocked OpenAI class
        service = OpenAIService()
        yield service

def test_openai_service_init(openai_service_instance, mock_openai_client):
    mock_openai_client.assert_called_once_with(api_key='test_api_key')
    assert openai_service_instance.embedding_model == 'text-embedding-ada-002'
    assert openai_service_instance.chat_model == 'gpt-3.5-turbo'

def test_get_embedding_success(openai_service_instance, mock_openai_client):
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_openai_client.return_value.embeddings.create.return_value = mock_response

    text_to_embed = "test text"
    embedding = openai_service_instance.get_embedding(text_to_embed)

    mock_openai_client.return_value.embeddings.create.assert_called_once_with(
        input=[text_to_embed.replace("\n", " ")],
        model='text-embedding-ada-002'
    )
    assert embedding == [0.1, 0.2, 0.3]

def test_get_embedding_api_error(openai_service_instance, mock_openai_client):
    mock_openai_client.return_value.embeddings.create.side_effect = Exception("OpenAI Embedding Error")
    text_to_embed = "test text"

    with pytest.raises(Exception, match="OpenAI Embedding Error"):
        openai_service_instance.get_embedding(text_to_embed)

    mock_openai_client.return_value.embeddings.create.assert_called_once_with(
        input=[text_to_embed.replace("\n", " ")],
        model='text-embedding-ada-002'
    )

def test_generate_content_success(openai_service_instance, mock_openai_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Generated OpenAI response"))]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    prompt = "Generate a response"
    response = openai_service_instance.generate_content(prompt)

    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
    assert response == "Generated OpenAI response"

def test_generate_content_api_error(openai_service_instance, mock_openai_client):
    mock_openai_client.return_value.chat.completions.create.side_effect = Exception("OpenAI Chat Error")
    prompt = "Generate a response"

    with pytest.raises(Exception, match="OpenAI Chat Error"):
        openai_service_instance.generate_content(prompt)

    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
