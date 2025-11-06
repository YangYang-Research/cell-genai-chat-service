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
        formatted_messages = Utils.format_agent_messages(req.messages)

        if not formatted_messages:
            return JSONResponse(status_code=400, content={"error": "No messages provided"})

        message_payload = {"messages": formatted_messages}
        
        return StreamingResponse(agent_stream.agent_streaming(chat_id=req.chat_session_id, message=message_payload, model_name=req.model_name, stream_mode="messages"), media_type="text/html")

    except Exception as e:
        logger.error(f"An error occurred: {e} \n TRACEBACK: ", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
