from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

@dataclass
class AppConfig(object):
    """Base configuration class."""
    
    app_name: str = os.getenv("APP_NAME", "Cell GenAI Chat Service")
    app_version: str = os.getenv("APP_VERSION", "0.0.0")
    api_version: str = "v1"
    
@dataclass
class AWSConfig(object):
    """AWS configuration class."""

    aws_region: str = os.getenv("AWS_REGION", "ap-southeast-1")
    
    bedrock_model_claude_text_id: str = os.getenv("BEDROCK_MODEL_CLAUDE_TEXT_ID", "")
    bedrock_model_claude_text_max_tokens: str = os.getenv("BEDROCK_MODEL_CLAUDE_TEXT_MAX_TOKENS", "2048")
    bedrock_model_claude_text_temperature: str = os.getenv("BEDROCK_MODEL_CLAUDE_TEXT_TEMPERATURE", "0.7")

    bedkrock_model_claude_vision_id: str = os.getenv("BEDROCK_MODEL_CLAUDE_VISION_ID", "")
    bedrock_model_claude_vision_max_tokens: str = os.getenv("BEDROCK_MODEL_CLAUDE_VISION_MAX_TOKENS", "2048")
    bedrock_model_claude_vision_temperature: str = os.getenv("BEDROCK_MODEL_CLAUDE_VISION_TEMPERATURE", "0.7")

    bedrock_knowledge_base_id: str = os.getenv("BEDROCK_KNOWLEDGE_BASE_ID", "")
    bedrock_guardrail_id: str = os.getenv("BEDROCK_GUARDRAIL_ID", "")
    bedrock_guardrail_version: str = os.getenv("BEDROCK_GUARDRAIL_VERSION", "")
    
@dataclass
class LogConfig(object):
    """Logging configuration class."""

    log_max_size: str = os.getenv("LOG_MAX_SIZE", "10485760")  # 10 MB
    log_max_backups: str = os.getenv("LOG_MAX_BACKUPS", "5")    # 5 backup files