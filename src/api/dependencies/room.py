from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from crud.room import room_crud
from models import Room


async def get_room(
    room_uid: UUID, db: AsyncSession = Depends(get_async_db)
) -> Optional[Room]:
    if found_room := await room_crud.get_by_uid(db=db, uid=room_uid):
        return found_room
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )
