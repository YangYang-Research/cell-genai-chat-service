from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# ------------------- User Schemas -------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}

# ------------------- Message Schemas -------------------

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    user_id: int

class MessageUpdate(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class MessageRead(MessageBase):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}

# ------------------- Tool Schemas -------------------

class ToolBase(BaseModel):
    name: str
    status: str
    host: Optional[str] = None
    api_key: Optional[str] = None
    cse_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    user_agent: Optional[str] = None

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    host: Optional[str] = None
    api_key: Optional[str] = None
    cse_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    user_agent: Optional[str] = None

class ToolRead(ToolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}

# ------------------- LLM Schemas -------------------

class LLMBase(BaseModel):
    name: str
    provider: str
    model_id: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    status: str

class LLMCreate(LLMBase):
    pass

class LLMUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    status: Optional[str] = None

class LLMRead(LLMBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}

# ------------------- Agent Schemas -------------------

class AgentBase(BaseModel):
    name: str
    knowledge_base_id: Optional[str] = None
    llm_id: int
    system_prompt: Optional[str] = None
    tools: Optional[List[Any]] = None  # stored JSON

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    knowledge_base_id: Optional[str] = None
    llm_id: Optional[int] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[Any]] = None

class AgentRead(AgentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
