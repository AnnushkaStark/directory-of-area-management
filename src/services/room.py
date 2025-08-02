from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.room import room_crud
from crud.room_type import room_type_crud
from crud.user import user_crud
from models import Room
from schemas.room import RoomCreate
from utils.errors import DomainError, ErrorCodes


async def _check_type(db: AsyncSession, schema: RoomCreate) -> RoomCreate:
    if not await room_type_crud.get_by_id(db=db, obj_id=schema.type_id):
        raise DomainError(ErrorCodes.ROOM_TYPE_NOT_FOUND)
    return schema


async def _get_users(db: AsyncSession, schema: RoomCreate) -> RoomCreate:
    if len(schema.users_ids):
        schema.users_ids = list(set(schema.users_ids))
        users = []
        for user_id in schema.users_ids:
            if user := await user_crud.get_by_id(db=db, obj_id=user_id):
                users.append(user)
        if len(users) < len(schema.users_ids):
            raise DomainError(ErrorCodes.NOT_ALL_USERS_WAS_FOUND)
        return users
    return []


async def manage_obj(
    db: AsyncSession, schema: RoomCreate, db_obj: Optional[Room] = None
) -> Optional[Room]:
    try:
        schema = await _check_type(db=db, schema=schema)
    except DomainError:
        raise DomainError(ErrorCodes.ROOM_TYPE_NOT_FOUND)
    try:
        users = await _get_users(db=db, schema=schema)
    except DomainError:
        raise DomainError(ErrorCodes.NOT_ALL_USERS_WAS_FOUND)
    del schema.users_ids
    if db_obj:
        room = await room_crud.update(
            db=db, update_data=schema, obj_id=db_obj.id, commit=False
        )
        room.users = users
        await db.commit()
        return room
    else:
        room = await room_crud.create(
            db=db, create_schema=schema, commit=False
        )
        room.users = users
        await db.commit()
        return room
