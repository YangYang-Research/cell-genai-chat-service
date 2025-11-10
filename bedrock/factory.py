import os
from helpers.config import ToolConfig
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
        self.tool_conf = ToolConfig()
        self.chat_converse = Converse()
        self.GENERAL_ASSISTANT_PROMPT = PromptFactory.load_agent_prompt()

    def get_enabled_tools(self):
        """Return a list of enabled tool instances."""
        tools = []

        if self.tool_conf.duckduckgo_search_enable == "enable":
            tools.append(DuckDuckGo)
        if self.tool_conf.arxiv_search_enable == "enable":
            tools.append(Arxiv)
        if self.tool_conf.wikipedia_search_enable == "enable":
            tools.append(Wikipedia)
        if self.tool_conf.google_search_enable == "enable":
            tools.append(GoogleSearch)
        if self.tool_conf.google_scholar_search_enable == "enable":
            tools.append(GoogleScholar)
        if self.tool_conf.google_trend_search_enable == "enable":
            tools.append(GoogleTrends)
        if self.tool_conf.asknews_search_enable == "enable":
            tools.append(AskNews)
        if self.tool_conf.reddit_search_enable == "enable":
            tools.append(RedditSearch)
        if self.tool_conf.searx_search_enable == "enable":
            tools.append(SearxSearch)
        if self.tool_conf.openweather_search_enable == "enable":
            tools.append(OpenWeather)

        return tools
    
    def agent(self, model_name: str):
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

        active_tools = self.get_enabled_tools()
        # print(f"[AgentFactory] Enabled tools: {[t.name for t in active_tools]}")

        # Create the LangChain agent
        return create_agent(
            system_prompt=self.GENERAL_ASSISTANT_PROMPT,
            tools=active_tools,
            model=llm,
        )

class LLMFactory:
    def __init__(self):
        self.tool_conf = ToolConfig()
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