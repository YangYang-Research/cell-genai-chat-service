import os
import boto3
from bedrock.converse import Converse
from langchain.agents import create_agent

class Agent():
    def __init__(self):
        self.chat_converse = Converse()
        self.GENERAL_ASSISTANT_PROMPT = self.load_general_assistant_prompt()

    def load_general_assistant_prompt(self) -> str:
        """Load system prompt for the general assistant agent."""
        prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/general-assistant.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip()
            return prompt_text
        except FileNotFoundError:
            raise FileNotFoundError(f"[Agent] Prompt file not found: {prompt_path}")

    def agent(self, model_name: str):      
        if model_name == "claude": 
            agent = create_agent(
                system_prompt=self.GENERAL_ASSISTANT_PROMPT,
                tools=[],
                model=self.chat_converse.claude_model_text()
            )
            return agent
        else:
            return None