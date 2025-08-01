from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.room_type import room_type_crud
from models import RoomType
from schemas.room_type import RoomTypeBase
from utils.errors import DomainError, ErrorCodes


async def manage_obj(
    db: AsyncSession, schema: RoomTypeBase, db_obj: Optional[RoomType] = None
) -> RoomType:
    if await room_type_crud.get_by_name(db=db, name=schema.name.upper()):
        raise DomainError(ErrorCodes.ROOM_TYPE_ALREADY_EXISTS)
    if db_obj:
        return await room_type_crud.update(
            db=db, db_obj=db_obj, update_data=schema
        )
    else:
        return await room_type_crud.create(db=db, create_schema=schema)
