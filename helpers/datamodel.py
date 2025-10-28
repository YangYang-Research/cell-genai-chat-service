from pydantic import BaseModel
from typing import List, Literal, Generator, Optional

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    model_id: Optional[str] = None
    model_name: Optional[str] = None
    messages: List[ChatMessage]