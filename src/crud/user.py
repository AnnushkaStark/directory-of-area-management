from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import User
from schemas.pagination import PaginationResponse
from schemas.user import UserBase, UserCreate, UserResponse

from .async_crud import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserBase, UserCreate]):
    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_uid(self, db: AsyncSession, uid: UUID) -> Optional[User]:
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.account),
            )
            .where(self.model.uid == uid)
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_multi(
        self, db: AsyncSession, offset: int = 0, limit: int = 20
    ) -> PaginationResponse[UserResponse]:
        statement = (
            select(self.model, func.count().over().label("total"))
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(statement)
        rows = result.mappings().all()
        return PaginationResponse.create(
            limit=limit,
            offset=offset,
            count=rows[0]["total"] if rows else 0,
            items=[r["User"] for r in rows],
        )


user_crud = UserCRUD(User)
