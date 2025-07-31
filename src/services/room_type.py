from sqlalchemy.ext.asyncio import AsyncSession

from crud.room_type import room_type_crud
from models import RoomType
from schemas.room_type import RoomTypeBase


async def create(db: AsyncSession, create_data: RoomTypeBase) -> RoomType:
    if await room_type_crud.get_by_name(db=db, name=create_data.name.upper()):
        raise Exception("Name room type alredy exsists")
    return await room_type_crud.create(db=db, create_schema=create_data)
