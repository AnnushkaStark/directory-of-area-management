from sqlalchemy.ext.asyncio import AsyncSession

from crud.room_type import room_type_crud
from models import RoomType
from schemas.room_type import RoomTypeBase
from utils.errors import DomainError, ErrorCodes


async def create(db: AsyncSession, create_data: RoomTypeBase) -> RoomType:
    if await room_type_crud.get_by_name(db=db, name=create_data.name.upper()):
        raise DomainError(ErrorCodes.ROOM_TYPE_ALREADY_EXISTS)
    return await room_type_crud.create(db=db, create_schema=create_data)


async def update(
    db: AsyncSession, update_data: RoomTypeBase, db_obj: RoomType
) -> RoomType:
    if await room_type_crud.get_by_name(db=db, name=update_data.name.upper()):
        raise DomainError(ErrorCodes.ROOM_TYPE_ALREADY_EXISTS)
    return await room_type_crud.update(
        db=db, db_obj=db_obj, update_data=update_data
    )
