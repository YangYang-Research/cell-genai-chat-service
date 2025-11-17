from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from databases.schemas import ToolCreate, ToolUpdate, ToolOut
from databases.crud import (
    create_tool, get_tools, get_tool, update_tool, delete_tool, get_enabled_tools
)
from databases.database import SessionLocal

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.post("/", response_model=ToolOut)
async def create_tool_route(data: ToolCreate, db: AsyncSession = Depends(SessionLocal)):
    return await create_tool(db, data)


@router.get("/", response_model=list[ToolOut])
async def list_tools_route(db: AsyncSession = Depends(SessionLocal)):
    return await get_tools(db)


@router.get("/enabled", response_model=list[ToolOut])
async def list_enabled_tools_route(db: AsyncSession = Depends(SessionLocal)):
    return await get_enabled_tools(db)


@router.get("/{tool_id}", response_model=ToolOut)
async def get_tool_route(tool_id: int, db: AsyncSession = Depends(SessionLocal)):
    tool = await get_tool(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.put("/{tool_id}", response_model=ToolOut)
async def update_tool_route(tool_id: int, data: ToolUpdate, db: AsyncSession = Depends(SessionLocal)):
    tool = await update_tool(db, tool_id, data)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.delete("/{tool_id}")
async def delete_tool_route(tool_id: int, db: AsyncSession = Depends(SessionLocal)):
    result = await delete_tool(db, tool_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tool not found")