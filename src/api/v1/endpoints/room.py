from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

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

router = APIRouter(prefix="/room", tags=["Room"])
