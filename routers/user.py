from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from databases.schemas import UserCreate, UserUpdate, UserOut
from databases.crud import (
    create_user, get_users, get_user, update_user, delete_user
)
from databases.database import SessionLocal

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_route(data: UserCreate, db: AsyncSession = Depends(SessionLocal)):
    return await create_user(db, data)


@router.get("/", response_model=list[UserOut])
async def list_users_route(db: AsyncSession = Depends(SessionLocal)):
    return await get_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def get_user_route(user_id: int, db: AsyncSession = Depends(SessionLocal)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user_route(user_id: int, data: UserUpdate, db: AsyncSession = Depends(SessionLocal)):
    user = await update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(user_id: int, db: AsyncSession = Depends(SessionLocal)):
    result = await delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
