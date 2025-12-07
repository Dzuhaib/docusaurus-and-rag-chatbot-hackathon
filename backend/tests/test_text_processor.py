import pytest
from unittest.mock import MagicMock, patch
import os
import json
from backend.src.qdrant_indexer.text_processor import TextProcessor

@pytest.fixture
def text_processor_instance():
    # Create a dummy docs_base_path for testing
    dummy_docs_path = "test_docs"
    os.makedirs(dummy_docs_path, exist_ok=True)
    yield TextProcessor(docs_base_path=dummy_docs_path)
    # Clean up
    if os.path.exists(dummy_docs_path):
        for root, dirs, files in os.walk(dummy_docs_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dummy_docs_path)

@pytest.fixture
def mock_gemini_env():
    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_gemini_key"}):
        yield

def test_text_processor_init(mock_gemini_env):
    processor = TextProcessor(docs_base_path=".")
    assert processor.gemini_api_key == "dummy_gemini_key"
    assert processor.embedding_model == "embedding-001"

def test_text_processor_init_no_gemini_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY not found in environment variables."):
            TextProcessor(docs_base_path=".")

def test_extract_frontmatter(text_processor_instance):
    content = "---\ntitle: Test Title\nauthor: Me\n---\nHello World"
    frontmatter = text_processor_instance._extract_frontmatter(content)
    assert frontmatter == {"title": "Test Title", "author": "Me"}

def test_clean_markdown(text_processor_instance):
    content = "---\ntitle: Test\n---\nHello ![alt](img.png) [link](url) <p>HTML</p>\n\n\nNew line"
    cleaned = text_processor_instance._clean_markdown(content)
    assert cleaned == "Hello New line"

def test_get_metadata_from_path(text_processor_instance):
    # Mock docs_base_path
    text_processor_instance.docs_base_path = os.path.abspath("test_docs")
    os.makedirs(os.path.join(text_processor_instance.docs_base_path, "chapter1"), exist_ok=True)

    # Test for subchapter
    file_path = os.path.join(text_processor_instance.docs_base_path, "chapter1", "subchapter_a.md")
    metadata = text_processor_instance._get_metadata_from_path(file_path)
    assert metadata["file_path"] == os.path.join("chapter1", "subchapter_a.md")
    assert metadata["chapter_title"] == "Chapter1" # Default fallback
    assert metadata["subchapter_title"] == "Subchapter A"

    # Test for _index.md
    file_path_index = os.path.join(text_processor_instance.docs_base_path, "chapter1", "_index.md")
    metadata_index = text_processor_instance._get_metadata_from_path(file_path_index)
    assert metadata_index["file_path"] == os.path.join("chapter1", "_index.md")
    assert metadata_index["subchapter_title"] == "Chapter1 Overview"

def test_process_markdown_file(text_processor_instance, mock_gemini_env):
    # Create a dummy markdown file
    file_path = os.path.join(text_processor_instance.docs_base_path, "test_doc.md")
    with open(file_path, "w") as f:
        f.write("---\ntitle: My Doc\n---\n# Heading 1\n\nParagraph 1.\n\nParagraph 2.")
    
    with patch('google.generativeai.embed_content', return_value={'embedding': [[0.1]*768]}):
        chunks = text_processor_instance.process_markdown_file(file_path)
        assert len(chunks) == 2 # Heading and two paragraphs become two chunks
        assert chunks[0]["text"] == "# Heading 1" # Markdown parsing doesn't remove headings
        assert chunks[1]["text"] == "Paragraph 1.\n\nParagraph 2." # Chunks are paragraphs
        assert "chunk_id" in chunks[0]
        assert chunks[0]["page_title"] == "My Doc"

def test_load_all_markdown_content(text_processor_instance, mock_gemini_env):
    os.makedirs(os.path.join(text_processor_instance.docs_base_path, "chapter1"), exist_ok=True)
    with open(os.path.join(text_processor_instance.docs_base_path, "chapter1", "doc1.md"), "w") as f:
        f.write("# Doc 1\nContent 1")
    with open(os.path.join(text_processor_instance.docs_base_path, "doc2.md"), "w") as f:
        f.write("# Doc 2\nContent 2")
    
    with patch('google.generativeai.embed_content', return_value={'embedding': [[0.1]*768]}):
        all_chunks = text_processor_instance.load_all_markdown_content()
        assert len(all_chunks) == 4 # Each doc has 2 chunks (heading + content)
        assert any(c["page_title"] == "Doc 1" for c in all_chunks)

def test_get_embeddings(text_processor_instance, mock_gemini_env):
    texts = ["text one", "text two"]
    mock_embedding = [[0.1]*768, [0.2]*768]
    with patch('google.generativeai.embed_content', return_value={'embedding': mock_embedding}) as mock_embed_content:
        embeddings = text_processor_instance.get_embeddings(texts)
        mock_embed_content.assert_called_once_with(
            model="embedding-001",
            content=texts,
            task_type="retrieval_query"
        )
        assert embeddings == mock_embedding

def test_get_embeddings_empty_texts(text_processor_instance):
    embeddings = text_processor_instance.get_embeddings([])
    assert embeddings == []
