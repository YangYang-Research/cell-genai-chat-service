from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str  # Plaintext password only during signup


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    user_id: int

class MessageRead(MessageBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class ChatResponse(BaseModel):
    user_message: str
    ai_response: str
