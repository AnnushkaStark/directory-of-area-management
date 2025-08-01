from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from api.dependencies.user import get_user
from crud.user import user_crud
from models import User
from schemas.account import AccountBase
from schemas.pagination import PaginationResponse
from schemas.user import UserCreate, UserFullResponse, UserResponse
from services import account as account_service
from services import user as user_service
from utils.errors import ErrorCodes, errs

__all__ = ["router"]

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=PaginationResponse[UserResponse])
async def read_users(
    offset: int = 0,
    limit: int = 0,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    return await user_crud.get_multi(db=db, offset=offset, limit=limit)


@router.get("/{user_uid}/", response_model=UserFullResponse)
async def read_user(
    db: AsyncSession = Depends(get_async_db), user: User = Depends(get_user)
):
    return user


@router.post(
    "/",
    responses=errs(
        e400=[
            ErrorCodes.EMAIL_ALREADY_REGISTERED,
            ErrorCodes.PASSWORDS_DONT_MATCH,
        ]
    ),
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserCreate, db: AsyncSession = Depends(get_async_db)
):
    return await user_service.create(db=db, create_data=create_data)


@router.patch("/{user_uid}/", status_code=status.HTTP_200_OK)
async def user_update(
    upadate_data: AccountBase,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_user),
):
    return await account_service.update(
        db=db, user_id=user.id, update_data=upadate_data
    )


@router.delete("/{user_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    db: AsyncSession = Depends(get_async_db), user: User = Depends(get_user)
):
    return await user_crud.remove(db=db, obj_id=user.id)
