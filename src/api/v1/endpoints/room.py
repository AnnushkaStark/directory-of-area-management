from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from api.dependencies.room import get_room
from crud.room import room_crud
from models import Room
from schemas.pagination import PaginationResponse
from schemas.room import RoomCreate, RoomFullResponse, RoomResponse
from services import room as room_service
from utils.errors import ErrorCodes, errs

__all__ = ["router"]

router = APIRouter(
    prefix="/room", tags=["Room"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=PaginationResponse[RoomResponse])
async def read_rooms(
    offset: int = 0, limit: int = 20, db: AsyncSession = Depends(get_async_db)
):
    return await room_crud.get_multi(db=db, offset=offset, limit=limit)


@router.get("/{room_uid}/", response_model=RoomFullResponse)
async def read_room(room: Room = Depends(get_room)):
    return room


@router.post(
    "/",
    responses=(
        _room_errs := errs(
            e400=[
                ErrorCodes.ROOM_TYPE_NOT_FOUND,
                ErrorCodes.USER_ID_MUST_BE_UNIQUE_FOR_ROOM,
                ErrorCodes.NOT_ALL_USERS_WAS_FOUND,
            ]
        )
    ),
    status_code=status.HTTP_201_CREATED,
)
async def cretate_room(
    schema: RoomCreate, db: AsyncSession = Depends(get_async_db)
):
    return await room_service.manage_obj(db=db, schema=schema)


@router.put(
    "/{room_uid}/", responses=_room_errs, status_code=status.HTTP_200_OK
)
async def update_room(
    schema: RoomCreate,
    db: AsyncSession = Depends(get_async_db),
    room: Room = Depends(get_room),
):
    return await room_service.manage_obj(db=db, db_obj=room, schema=schema)


@router.delete("/{room_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_room(
    db: AsyncSession = Depends(get_async_db), room: Room = Depends(get_room)
):
    await room_crud.remove(db=db, obj_id=room.id)
