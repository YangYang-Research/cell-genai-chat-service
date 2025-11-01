import traceback
from bedrock.agent import AgentFactory
from typing import List, Literal, Generator, Optional
from helpers.loog import logger
from fastapi.responses import JSONResponse

class Streaming():
    def __init__(self):
        self.agent = AgentFactory()
        
    def agent_streaming(self, chat_id: str, message: dict, model_name: str, stream_mode: str) -> Generator[str, None, None]:
        try:
            agent = self.agent.agent(model_name=model_name)
            if agent:
                # The ReAct agent returns a dict with 'output'
                for token, metadata in agent.stream(input=message, stream_mode=stream_mode):
                    if metadata.get("langgraph_node") == "model":
                        content_blocks = token.content_blocks or []
                        for block in content_blocks:
                            if block.get("type") == "text":
                                text = block.get("text", "")
                                if text.strip():
                                    yield text
                yield "\n"
            else:
                yield f"Model {model_name} not found."
        except Exception as e:
            yield f"\n[Error] {str(e)}"
            logger.error(f"An error occurred: {e} \n TRACEBACK: ", traceback.format_exc())
    