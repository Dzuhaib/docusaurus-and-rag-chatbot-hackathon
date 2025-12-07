from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uuid

class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = Field(default=None, description="The user-selected text from the page to provide context.")
    history: Optional[List[Dict[str, str]]] = Field(default=None, description="Previous messages in the conversation for context.")

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, str]]] = Field(default=None, description="List of source documents used for the response.")
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID for the message.")

class FeedbackRequest(BaseModel):
    message_id: str
    query: str
    response: str
    sources: Optional[List[Dict[str, str]]]
    rating: str # e.g., "good" or "bad"
    context: Optional[str]
