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
    api_ver_1: str = "v1"
    
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

@dataclass
class ToolConfig(object):
    """Tool configuration class."""
    duckduckgo_search_enable: str = os.getenv("DUCKDUCKGO_SEARCH_ENABLE", "enable")

    arxiv_search_enable: str = os.getenv("ARXIV_SEARCH_ENABLE", "enable")
    
    wikipedia_search_enable: str = os.getenv("WIKIPEDIA_SEARCH_ENABLE", "enable")

    google_search_enable: str = os.getenv("GOOGLE_SEARCH_ENABLE", "disable")
    google_search_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    google_search_cse_id: str = os.getenv("GOOGLE_API_KEY", "")

    google_scholar_search_enable: str = os.getenv("GOOGLE_SCHOLAR_SEARCH_ENABLE", "disable")
    google_scholar_serp_api_key: str = os.getenv("GOOGLE_SCHOLAR_SERP_API_KEY", "")
    
    google_trend_search_enable: str = os.getenv("GOOGLE_TREND_SEARCH_ENABLE", "disable")
    google_trend_serp_api_key: str = os.getenv("GOOGLE_TREND_SERP_API_KEY", "")

    asknews_search_enable: str = os.getenv("ASKNEWS_SEARCH_ENABLE", "disable")
    asknews_client_id: str = os.getenv("ASKNEWS_CLIENT_ID", "")
    asknews_client_secret: str = os.getenv("ASKNEWS_CLIENT_SECRET", "")

    reddit_search_enable: str = os.getenv("REDDIT_SEARCH_ENABLE", "disable")
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_user_agent: str = os.getenv("REDDIT_USER_AGENT", "")

    searx_search_enable: str = os.getenv("SEARX_SEARCH_ENABLE", "")
    searx_host: str = os.getenv("SEARX_HOST", "")

    openweather_search_enable: str = os.getenv("OPENWEATHER_SEARCH_ENABLE", "disable")
    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")