import traceback
from bedrock.agent import Agent
from typing import List, Literal, Generator, Optional

class Streaming():
    def __init__(self):
        self.agent = Agent()
        
    def agent_streaming(self, messages, stream_mode) -> Generator[str, None, None]:
        try:
            cell_agent = self.agent.cell_agent()
            # The ReAct agent returns a dict with 'output'
            for token, metadata in cell_agent.stream(messages, stream_mode=stream_mode):
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
    