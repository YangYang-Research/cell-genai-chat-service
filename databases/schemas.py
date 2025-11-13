from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# ---------------- User Schemas ----------------
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
        from_attributes = True

# ---------------- Message Schemas ----------------
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    user_id: int

class MessageRead(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    user_message: str
    ai_response: str

# ---------------- ToolConfig Schemas ----------------
class ToolConfigBase(BaseModel):
    name: str
    status: Optional[str] = "enable"
    host: Optional[str] = None
    api_key: Optional[str] = None
    cse_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    user_agent: Optional[str] = None

class ToolConfigCreate(ToolConfigBase):
    """Schema for creating a new tool config."""
    pass

class ToolConfigUpdate(BaseModel):
    """Schema for updating an existing tool config."""
    status: Optional[str] = None
    host: Optional[str] = None
    api_key: Optional[str] = None
    cse_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    user_agent: Optional[str] = None

class ToolConfigRead(ToolConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
