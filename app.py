from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Generator, Optional
import boto3
import traceback
import uvicorn
from helpers.config import AppConfig, AWSConfig
from bedrock.stream import Streaming
# LangChain / Bedrock
from langchain_aws import ChatBedrockConverse
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

app_conf = AppConfig()
aws_conf = AWSConfig()
agent_stream = Streaming()
# =====================================
# FastAPI setup
# =====================================
app = FastAPI(title="Cell GenAI Chat Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    model_id: Optional[str] = None
    messages: List[ChatMessage]

def format_messages(messages: List[ChatMessage]):
    formatted = []
    for msg in messages:
        if msg.role == "user":
            formatted.append(HumanMessage(content=msg.content))
        else:
            formatted.append(AIMessage(content=msg.content))
    return formatted

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/chat/agent/completions")
def chat_agent_completions(req: ChatRequest):
    """
    Streaming chat endpoint using AWS Bedrock (Claude) + ReAct agent.
    """
    try:
        messages = format_messages(req.messages)
        last_user_msg = messages[-1].content if messages else "Hello!"
        
        history = [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
            for m in messages[:-1]
        ]

        input_payload = {
            "input": last_user_msg,
            "chat_history": history
        }
        

        return StreamingResponse(agent_stream.agent_streaming(input_payload, "messages"), media_type="text/plain")

    except Exception as e:
        print("ERROR:", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
