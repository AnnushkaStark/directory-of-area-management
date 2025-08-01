import uuid
from typing import Literal

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.user import user_crud
from models import User


async def get_user(
    user_uid: uuid.UUID | Literal["me"],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    if user_uid == "me":
        return await user_crud.get_by_uid(db=db, uid=user.uid)
    return await user_crud.get_by_uid(db=db, uid=user_uid)
