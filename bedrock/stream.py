import traceback
from bedrock.agent import Agent
from typing import List, Literal, Generator, Optional

class Streaming():
    def __init__(self):
        self.agent = Agent()
        
    def agent_streaming(self, message, model_name, model_id, stream_mode) -> Generator[str, None, None]:
        try:
            agent = self.agent.agent(model_name=model_name, model_id=model_id)
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
        except Exception as e:
            yield f"\n[Error] {str(e)}"
            print("TRACE:", traceback.format_exc())
    