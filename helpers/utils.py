from typing import List, Literal, Generator, Optional
from helpers.datamodel import ChatMessage, ChatRequest
from langchain_core.messages import HumanMessage, AIMessage

class Utils:
    def __init__(self):
        pass

    def format_agent_messages(messages: List[ChatMessage]):
        formatted = []
        for msg in messages:
            if msg.role == "user":
                formatted.append(HumanMessage(content=msg.content))
            else:
                formatted.append(AIMessage(content=msg.content))
        return formatted
