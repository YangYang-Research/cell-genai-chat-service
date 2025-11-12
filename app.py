import uvicorn
import traceback
from fastapi import FastAPI, Request
from helpers.utils import Utils
from databases.base import Base
from helpers.loog import logger
from bedrock.stream import Streaming
import databases.models as db_models
from contextlib import asynccontextmanager
from helpers.config import AppConfig, AWSConfig
from fastapi.middleware.cors import CORSMiddleware
from helpers.datamodel import ChatAgentRequest, ChatLLMRequest
from fastapi.responses import StreamingResponse, JSONResponse
from databases.database import engine, create_database_if_not_exists

app_conf = AppConfig()
aws_conf = AWSConfig()
streaming = Streaming()

# ------------------- FastAPI App -------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    await create_database_if_not_exists()

    async with engine.begin() as conn:
        await conn.run_sync(db_models.Base.metadata.create_all)
    print("✅ Tables synchronized with models.")

    yield  # <-- Application runs here

    # --- Shutdown ---
    await engine.dispose()
    print("🧹 Database connection closed.")

app = FastAPI(title=app_conf.app_name, version=app_conf.app_version, lifespan=lifespan)

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

@app.post(f"/{app_conf.api_ver_1}/chat/agent/completions")
async def chat_agent_completions(req: ChatAgentRequest, http_req: Request):
    try:
        authorization_header = http_req.headers.get("Authorization")
        if not authorization_header:
            return JSONResponse(status_code=401, content={
                "msg": "Missing authorization header"
            })
        
        if Utils.check_api_authentication(authorization_header):

            formatted_messages = Utils.format_agent_messages(req.messages)

            if not formatted_messages:
                return JSONResponse(status_code=400, content={"error": "No messages provided"})

            message_payload = {"messages": formatted_messages}
            
            return StreamingResponse(streaming.agent_astreaming(chat_id=req.chat_session_id, message=message_payload, model_name=req.model_name, stream_mode="messages"), media_type="text/html")
        else:
            return JSONResponse(status_code=403, content={
                "msg": "Invalid credential",
            })
    except Exception as e:
        logger.error(f"An error occurred: {e} \n TRACEBACK: ", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post(f"/{app_conf.api_ver_1}/chat/llm/completions")
async def chat_llm_completions(req: ChatLLMRequest, http_req: Request):
    try:
        authorization_header = http_req.headers.get("Authorization")
        if not authorization_header:
            return JSONResponse(status_code=401, content={
                "msg": "Missing authorization header"
            })
        
        if Utils.check_api_authentication(authorization_header):
            formatted_messages = Utils.format_agent_messages(req.messages)

            if not formatted_messages:
                return JSONResponse(status_code=400, content={"error": "No messages provided"})
            
            message_payload = {"messages": formatted_messages}

            return StreamingResponse(streaming.llm_astreaming(chat_id=req.chat_session_id, message=message_payload, model_name=req.model_name), media_type="text/html")
        else:
            return JSONResponse(status_code=403, content={
                "msg": "Invalid credential",
            })
    except Exception as e:
        logger.error(f"An error occurred: {e} \n TRACEBACK: ", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
