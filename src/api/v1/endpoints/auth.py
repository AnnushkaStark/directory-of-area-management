from fastapi import APIRouter, Depends, status, Security, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt import JwtAuthorizationCredentials
from api.dependencies.database import get_async_db
from utils.errors import ErrorCodes, errs
from schemas.user import UserLogin
from schemas.token import TokenAccessRefresh
from services import user as user_service
from utils.security.security import access_security, refresh_security, create_tokens
from config.configs import jwt_settings


__all__ = ["router"]

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", status_code=status.HTTP_200_OK, responses=errs(e400=[ErrorCodes.INVALID_PASSWORD, ErrorCodes.EMAIL_NOT_FOUND]))
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    return await user_service.login(db=db, login_data=login_data)


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)


@router.delete("/", status_code=status.HTTP_200_OK)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response()
    response.delete_cookie(jwt_settings.ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(jwt_settings.REFRESH_TOKEN_COOKIE_KEY)
    return response

