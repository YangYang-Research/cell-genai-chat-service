from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from databases.base import Base

class AWSConfigModel(Base):
    __tablename__ = "aws_config"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    aws_region = Column(String(64), default="ap-southeast-1")
    aws_secret_name = Column(String(255), nullable=True)

    # Claude Text model
    bedrock_model_claude_text_id = Column(String(255), nullable=True)
    bedrock_model_claude_text_max_tokens = Column(String(16), default="2048")
    bedrock_model_claude_text_temperature = Column(String(8), default="0.7")

    # Claude Vision model
    bedrock_model_claude_vision_id = Column(String(255), nullable=True)
    bedrock_model_claude_vision_max_tokens = Column(String(16), default="2048")
    bedrock_model_claude_vision_temperature = Column(String(8), default="0.7")

    # Knowledge Base
    bedrock_knowledge_base_id = Column(String(255), nullable=True)

    # Guardrails
    bedrock_guardrail_id = Column(String(255), nullable=True)
    bedrock_guardrail_version = Column(String(64), nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ToolConfigModel(Base):
    __tablename__ = "tool_config"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Tool identification
    name = Column(String(64), nullable=False, unique=True)  # e.g., "duckduckgo", "arxiv"
    status = Column(String(16), default="disable")           # "enable" or "disable"
    
    # Optional authentication / API credentials
    host = Column(String(255), nullable=True)
    api_key = Column(String(255), nullable=True)
    cse_id = Column(String(255), nullable=True)
    client_id = Column(String(255), nullable=True)
    client_secret = Column(String(255), nullable=True)
    user_agent = Column(String(255), nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One-to-many relationship — A role can have many users
    users = relationship("UserModel", back_populates="role")

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    changed_password = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role = relationship("RoleModel", back_populates="users")
    messages = relationship("MessageModel", back_populates="user")

class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(10))  # "user" or "assistant"
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="messages")
