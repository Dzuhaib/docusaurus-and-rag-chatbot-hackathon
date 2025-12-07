import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            self.client = None # Client will be None if API key is not set
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
        self.chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")

    def _check_client(self):
        if not self.client:
            raise ValueError("OpenAI API key is not set. Please set OPENAI_API_KEY in your .env file.")

    def get_embedding(self, text: str) -> list[float]:
        self._check_client()
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(input=[text], model=self.embedding_model)
        return response.data[0].embedding

    def generate_content(self, prompt: str) -> str:
        self._check_client()
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

openai_service = OpenAIService()
