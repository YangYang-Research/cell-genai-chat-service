from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from databases.schemas import AgentCreate, AgentUpdate, AgentOut
from databases.crud import (
    create_agent, get_agents, get_agent, update_agent, delete_agent
)
from databases.database import SessionLocal

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=AgentOut)
async def create_agent_route(data: AgentCreate, db: AsyncSession = Depends(SessionLocal)):
    print("DEBUG")
    return await create_agent(db, data)


@router.get("/", response_model=list[AgentOut])
async def list_agents_route(db: AsyncSession = Depends(SessionLocal)):
    print("DEBUG")
    return await get_agents(db)


@router.get("/{agent_id}", response_model=AgentOut)
async def get_agent_route(agent_id: int, db: AsyncSession = Depends(SessionLocal)):
    agent = await get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentOut)
async def update_agent_route(agent_id: int, data: AgentUpdate, db: AsyncSession = Depends(SessionLocal)):
    agent = await update_agent(db, agent_id, data)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.delete("/{agent_id}")
async def delete_agent_route(agent_id: int, db: AsyncSession = Depends(SessionLocal)):
    result = await delete_agent(db, agent_id)
    if not result:
        raise HTTPException(status_code=404, detail="Agent not found")
