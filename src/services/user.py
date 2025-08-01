from argon2.exceptions import Argon2Error
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserCreate, UserLogin
from services import account as account_service
from utils.errors import DomainError, ErrorCodes
from utils.security.password_hasher import get_password_hash, verify_password
from utils.security.security import TokenSubject, create_tokens


async def create(db: AsyncSession, create_data: UserCreate) -> User:
    if await user_crud.get_by_email(db=db, email=create_data.email):
        raise DomainError(ErrorCodes.EMAIL_ALREADY_REGISTERED)
    if create_data.password != create_data.password_confirm:
        raise DomainError(ErrorCodes.PASSWORDS_DONT_MATCH)
    create_data.password = await get_password_hash(
        password=create_data.password
    )
    del create_data.password_confirm
    user = await user_crud.create(db=db, create_schema=create_data)
    await account_service.create(
        db=db, create_schema=create_data, user_id=user.id
    )
    return user


async def login(db: AsyncSession, login_data: UserLogin) -> dict:
    found_user = await user_crud.get_by_email(db=db, email=login_data.email)
    if not found_user:
        raise DomainError(ErrorCodes.EMAIL_NOT_FOUND)
    try:
        await verify_password(
            plain_password=login_data.password,
            hashed_password=found_user.password,
        )
    except Argon2Error:
        raise Exception("Invalid password")

    subject = TokenSubject(
        uid=str(found_user.uid),
        email=found_user.email,
    )
    return await create_tokens(subject)
