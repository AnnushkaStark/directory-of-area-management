from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from api.dependencies.room_type import get_room_type
from crud.room_type import room_type_crud
from models import RoomType
from schemas.pagination import PaginationResponse
from schemas.room_type import RoomTypeBase, RoomTypeResponse
from services import room_type as room_type_service
from utils.errors import ErrorCodes, errs

__all__ = ["router"]

router = APIRouter(prefix="/room_type", tags=["RoomType"])


@router.get("/", response_model=PaginationResponse[RoomTypeResponse])
async def read_room_types(
    offset: int = 0, limit: int = 20, db: AsyncSession = Depends(get_async_db)
):
    return await room_type_crud.get_multi(db=db, offset=offset, limit=limit)


@router.get("/{room_type_uid}/", response_model=RoomTypeResponse)
async def read_room_type(room_type: RoomType = Depends(get_room_type)):
    return room_type


@router.post(
    "/",
    responses=errs(e400=ErrorCodes.ROOM_TYPE_ALREADY_EXISTS),
    status_code=status.HTTP_201_CREATED,
)
async def room_type_create(
    room_type: RoomTypeBase, db: AsyncSession = Depends(get_async_db)
):
    return await room_type_service.create(db=db, create_data=room_type)


@router.put(
    "/{room_type_uid}/",
    responses=errs(ErrorCodes.ROOM_TYPE_ALREADY_EXISTS),
    status_code=status.HTTP_200_OK,
)
async def room_type_update(
    update_data: RoomTypeBase,
    room_type: RoomType = Depends(get_room_type),
    db: AsyncSession = Depends(get_async_db),
):
    return await room_type_service.update(
        db=db, db_obj=room_type, update_data=update_data
    )


@router.delete("/{room_type_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_room_type(
    room_type: RoomType = Depends(get_room_type),
    db: AsyncSession = Depends(get_async_db),
):
    await room_type_crud.remove(db=db, obj_id=room_type.id)
