import os
from databases.crud import get_enabled_tools
from databases.database import SessionLocal
from bedrock.converse import Converse
from langchain.agents import create_agent
from tools.web_search import (
    DuckDuckGo,
    Arxiv,
    Wikipedia,
    GoogleSearch,
    GoogleScholar,
    GoogleTrends,
    AskNews,
    RedditSearch,
    SearxSearch,
    OpenWeather,
)

TOOL_CLASS_MAP = {
    "duckduckgo": DuckDuckGo,
    "arxiv": Arxiv,
    "wikipedia": Wikipedia,
    "google_search": GoogleSearch,
    "google_scholar": GoogleScholar,
    "google_trends": GoogleTrends,
    "asknews": AskNews,
    "reddit": RedditSearch,
    "searx": SearxSearch,
    "openweather": OpenWeather
}

class PromptFactory:
    def __init__(self):
        pass
    
    def load_agent_prompt() -> str:
        """Load system prompt for the agent."""
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/agent-prompt.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"[Agent] Prompt file not found: {prompt_path}")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
        
    def load_llm_prompt() -> str:
        """Load system prompt for the llm."""
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/llm-prompt.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"[Agent] Prompt file not found: {prompt_path}")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
        
class AgentFactory:
    """Factory for creating LangChain agents with dynamically enabled tools."""

    def __init__(self):
        self.chat_converse = Converse()
        self.GENERAL_ASSISTANT_PROMPT = PromptFactory.load_agent_prompt()

    async def get_enabled_tools(self):
        """Fetch all enabled tools from the DB and return a list of tool classes."""
        tools = []
        async with SessionLocal() as session:
            db_tools = await get_enabled_tools(session)

            for t in db_tools:
                tool_cls = TOOL_CLASS_MAP.get(t.name)
                if tool_cls:
                    tools.append(tool_cls)

        return tools
    
    async def agent(self, model_name: str):
        """Create and return an LLM agent with appropriate model and tools."""
        model_name = (model_name or "").lower()

        if model_name == "claude":
            llm = self.chat_converse.claude_model_text()
        elif model_name == "llama":
            # llm = self.chat_converse.titan_model_text()
            return None
        elif model_name == "gpt-oss":
            # llm = self.chat_converse.mistral_model_text()
            return None
        else:
            raise ValueError(f"[Agent] Unsupported model: {model_name}")

        active_tools = await self.get_enabled_tools()

        # Create the LangChain agent
        return create_agent(
            system_prompt=self.GENERAL_ASSISTANT_PROMPT,
            tools=active_tools,
            model=llm,
        )

class LLMFactory:
    def __init__(self):
        self.chat_converse = Converse()
    
    def llm(self, model_name: str):
        """Create and return an LLM model."""
        model_name = (model_name or "").lower()

        if model_name == "claude":
            llm = self.chat_converse.claude_model_text()
        elif model_name == "llama":
            # llm = self.chat_converse.titan_model_text()
            return None
        elif model_name == "gpt-oss":
            # llm = self.chat_converse.mistral_model_text()
            return None
        else:
            raise ValueError(f"[Agent] Unsupported model: {model_name}")
        
        return llm