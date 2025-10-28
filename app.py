import boto3
import uvicorn
import traceback
from fastapi import FastAPI
from helpers.utils import Utils
from helpers.loog import logger
from bedrock.stream import Streaming
from helpers.config import AppConfig, AWSConfig
from fastapi.middleware.cors import CORSMiddleware
from helpers.datamodel import ChatMessage, ChatRequest
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.responses import StreamingResponse, JSONResponse

app_conf = AppConfig()
aws_conf = AWSConfig()
agent_stream = Streaming()

# ------------------- FastAPI App -------------------
app = FastAPI(title="Cell GenAI Chat Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- API Endpoint -------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/chat/agent/completions")
def chat_agent_completions(req: ChatRequest):
    try:
        messages = Utils.format_agent_messages(req.messages)
        last_user_msg = messages[-1].content if messages else "Hello!"
        
        history = [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
            for m in messages[:-1]
        ]

        message_payload = {
            "messages": history + [
                {"role": "user", "content": last_user_msg}
            ]
        }
        
        return StreamingResponse(agent_stream.agent_streaming(message=message_payload, model_name=req.model_name, model_id=req.model_id, stream_mode="messages"), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"An error occurred: {e} \n TRACEBACK: ", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
