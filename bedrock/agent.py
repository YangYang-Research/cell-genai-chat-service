import os
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
    Weather,
)

class Agent:
    def __init__(self):
        self.chat_converse = Converse()
        self.GENERAL_ASSISTANT_PROMPT = self.load_general_assistant_prompt()

    def load_general_assistant_prompt(self) -> str:
        """Load system prompt for the general assistant agent."""
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/general-assistant.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"[Agent] Prompt file not found: {prompt_path}")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()

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

        # ✅ Create the LangChain agent
        agent = create_agent(
            system_prompt=self.GENERAL_ASSISTANT_PROMPT,
            tools=[DuckDuckGo, Arxiv, Wikipedia, GoogleSearch, GoogleScholar, GoogleTrends, AskNews, RedditSearch, SearxSearch, Weather],
            model=llm,
        )
        return agent
