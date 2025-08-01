from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from crud.room_type import room_type_crud
from models.room_type import RoomType


async def get_room_type(
    room_type_uid: UUID, db: AsyncSession = Depends(get_async_db)
) -> Optional[RoomType]:
    if found_room_type := await room_type_crud.get_by_uid(
        db=db, uid=room_type_uid
    ):
        return found_room_type
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found"
    )
