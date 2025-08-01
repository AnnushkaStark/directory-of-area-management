import uuid
from typing import Literal

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.user import user_crud
from models import User


async def user_uid(
    user_uid: uuid.UUID | Literal["me"],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> uuid.UUID:
    if user_uid == "me":
        return user.uid
    return user_uid


async def get_user(
    user_uid: uuid.UUID | Literal["me"] = Depends(user_uid),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    if found_user := await user_crud.get_by_uid(db=db, uid=user_uid):
        return found_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
