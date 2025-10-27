import os
import boto3
from bedrock.model import Model
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse

class Agent():
    def __init__(self):
        self.model = Model()
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

    def cell_agent(self):       
        agent = create_agent(
            system_prompt=self.GENERAL_ASSISTANT_PROMPT,
            tools=[],
            model=self.model.claude_model_text()
        )
        return agent