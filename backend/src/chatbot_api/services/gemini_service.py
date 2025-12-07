import google.generativeai as genai
from ..config import settings
from typing import List, Union, AsyncIterator # Changed Iterator to AsyncIterator

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_embedding(text: str) -> List[float]:
    """Generates an embedding for the given text using the configured Gemini embedding model."""
    try:
        response = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Depending on requirements, could re-raise, return empty, or a default
        raise

async def generate_content(prompt: str, stream: bool = False) -> Union[str, AsyncIterator[str]]: # Made async
    """Generates content using the configured Gemini generative model."""
    try:
        model = genai.GenerativeModel(model_name=settings.GENERATIVE_MODEL)
        if stream:
            async def generate_stream(): # Made async generator
                async for chunk in await model.generate_content_async(prompt, stream=True): # Use await and async for
                    if chunk.text:
                        yield chunk.text
            return generate_stream()
        else:
            response = await model.generate_content_async(prompt) # Use await for non-streaming
            return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        raise
