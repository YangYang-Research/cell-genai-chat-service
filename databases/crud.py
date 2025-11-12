from sqlalchemy.future import select
from databases import models, schemas

async def create_message(db, message: schemas.MessageCreate):
    db_msg = models.Message(**message.dict())
    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)
    return db_msg

async def get_user_messages(db, user_id: int):
    result = await db.execute(select(models.Message).where(models.Message.user_id == user_id))
    return result.scalars().all()
