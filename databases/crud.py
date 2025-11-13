from sqlalchemy.future import select
from databases import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession

# ---------------- Message CRUD (existing) ----------------
async def create_message(db: AsyncSession, message: schemas.MessageCreate):
    db_msg = models.MessageModel(**message.dict())
    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)
    return db_msg


async def get_user_messages(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.MessageModel).where(models.MessageModel.user_id == user_id)
    )
    return result.scalars().all()


# ---------------- ToolConfig CRUD (new) ----------------
async def get_enabled_tools(db: AsyncSession):
    """Return all ToolConfigModel rows with status 'enable'."""
    result = await db.execute(
        select(models.ToolConfigModel).where(models.ToolConfigModel.status == "enable")
    )
    return result.scalars().all()


async def get_tool_by_name(db: AsyncSession, tool_name: str):
    """Return a ToolConfigModel by its name."""
    result = await db.execute(
        select(models.ToolConfigModel).where(models.ToolConfigModel.name == tool_name)
    )
    return result.scalars().first()


async def create_tool(db: AsyncSession, tool: schemas.ToolConfigCreate):
    """Create a new tool configuration."""
    db_tool = models.ToolConfigModel(**tool.dict())
    db.add(db_tool)
    await db.commit()
    await db.refresh(db_tool)
    return db_tool


async def update_tool_status(db: AsyncSession, tool_name: str, status: str):
    """Update the status of a tool ('enable'/'disable')."""
    db_tool = await get_tool_by_name(db, tool_name)
    if not db_tool:
        raise ValueError(f"Tool '{tool_name}' not found")
    db_tool.status = status
    db.add(db_tool)
    await db.commit()
    await db.refresh(db_tool)
    return db_tool
