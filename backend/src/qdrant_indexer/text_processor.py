import os
import re
import hashlib
import json
import logging
from typing import List, Dict, Any, Optional
from markdown_it import MarkdownIt
from dotenv import load_dotenv
import google.generativeai as genai
import uuid

load_dotenv() # Load environment variables

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, docs_base_path: str):
        self.docs_base_path = os.path.abspath(docs_base_path)
        self.md = MarkdownIt()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self._init_gemini_model()

    def _init_gemini_model(self):
        genai.configure(api_key=self.gemini_api_key)
        # Using the embedding-001 model which provides 768 dimensions
        self.embedding_model = "gemini-embedding-001"
        try:
            # Test model availability
            genai.embed_content(model=self.embedding_model, content="test")
            logger.info(f"Initialized Google Gemini embedding model: {self.embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Gemini embedding model: {e}")
            raise

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extracts YAML frontmatter from Markdown content."""
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            frontmatter_str = match.group(1)
            frontmatter = {}
            for line in frontmatter_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"')
            return frontmatter
        return {}

    def _clean_markdown(self, content: str) -> str:
        """Removes frontmatter and image/link syntax from markdown."""
        # Remove frontmatter
        content = re.sub(r'^---\n(.*?)\n---\n', '', content, flags=re.DOTALL)
        # Remove image links: ![alt text](url)
        content = re.sub(r'!\s*\[.*?\]\s*\(.*?\)', '', content)
        # Remove regular links: [link text](url)
        content = re.sub(r'\[.*?\]\s*\(.*?\)', '', content)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Replace multiple newlines with single newline
        content = re.sub(r'\n\s*\n', '\n\n', content)
        return content.strip()

    def _get_metadata_from_path(self, file_path: str) -> Dict[str, Any]:
        """Extracts metadata like chapter, subchapter, URL from file path."""
        relative_path = os.path.relpath(file_path, self.docs_base_path)
        parts = relative_path.split(os.sep)

        metadata = {
            "file_path": relative_path,
            "url": f"/docs/{os.path.splitext(relative_path)[0]}", # Docusaurus URL format
        }

        if len(parts) >= 2 and parts[0].startswith('chapter'):
            metadata["chapter_dir"] = parts[0]
            # Try to get chapter title from _category_.json
            category_file = os.path.join(self.docs_base_path, parts[0], '_category_.json')
            if os.path.exists(category_file):
                try:
                    with open(category_file, 'r', encoding='utf-8') as f:
                        category_data = json.load(f)
                        metadata["chapter_title"] = category_data.get("label")
                except Exception:
                    metadata["chapter_title"] = parts[0].replace('-', ' ').title() # Fallback
            else:
                metadata["chapter_title"] = parts[0].replace('-', ' ').title() # Fallback
            
            # Corrected logic for sub-chapters
            subchapter_filename = os.path.splitext(parts[1])[0]
            if subchapter_filename == '_index':
                metadata["subchapter_title"] = metadata["chapter_title"] + " Overview"
            else:
                metadata["subchapter_title"] = subchapter_filename.replace('-', ' ').title()


        return metadata

    def process_markdown_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a markdown file, chunks its content, extracts metadata,
        and prepares data for embedding.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = self._extract_frontmatter(content)
        cleaned_content = self._clean_markdown(content)
        
        # Split content by double newlines to get paragraphs/chunks
        chunks = [chunk.strip() for chunk in cleaned_content.split('\n\n') if chunk.strip()]
        
        processed_chunks = []
        page_title = frontmatter.get('title', os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ').title())

        for i, chunk_text in enumerate(chunks):
            # Generate a unique ID for the chunk
            # Combination of file_path and chunk index
            chunk_id_str = f"{file_path}-{i}-{chunk_text[:50]}"
            # Generate a UUID5 from the SHA256 hash
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, hashlib.sha256(chunk_id_str.encode()).hexdigest()))

            metadata = {
                "text": chunk_text,
                "chunk_id": chunk_id,
                "page_title": page_title,
                **self._get_metadata_from_path(file_path),
                **frontmatter # Frontmatter overrides path-derived metadata
            }
            # Remove redundant keys if frontmatter was used
            metadata.pop('title', None)
            metadata.pop('slug', None) # Remove slug if present in frontmatter

            processed_chunks.append(metadata)
        
        return processed_chunks

    def load_all_markdown_content(self) -> List[Dict[str, Any]]:
        """
        Loads and processes all markdown content from the docs_base_path.
        """
        all_processed_chunks = []
        for root, _, files in os.walk(self.docs_base_path):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    all_processed_chunks.extend(self.process_markdown_file(file_path))
        return all_processed_chunks

    def get_embeddings(self, texts: List[str], task_type: str = "retrieval_document") -> List[List[float]]:
        """
        Generates embeddings for a list of texts using the configured Gemini model.
        
        Args:
            texts: A list of strings to embed.
            task_type: The task type for embedding (e.g., "retrieval_query", "retrieval_document").
                       Defaults to "retrieval_document".
        """
        if not texts:
            return []
        
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=texts,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embeddings with task_type '{task_type}': {e}")
            raise