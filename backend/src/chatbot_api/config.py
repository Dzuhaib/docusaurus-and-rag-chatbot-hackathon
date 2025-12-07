from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    GENERATIVE_MODEL_PROVIDER: str = os.getenv("GENERATIVE_MODEL_PROVIDER", "gemini") # "gemini" or "openai"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
    GENERATIVE_MODEL: str = os.getenv("GENERATIVE_MODEL", "gemini-pro")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
    
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_content")
    

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
