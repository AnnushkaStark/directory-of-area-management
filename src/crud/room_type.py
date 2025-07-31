from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import RoomType
from schemas.pagination import PaginationResponse
from schemas.room_type import RoomTypeBase, RoomTypeResponse

from .async_crud import BaseAsyncCRUD


class RoomTypeCRUD(BaseAsyncCRUD[RoomType, RoomTypeBase, RoomTypeResponse]):
    async def get_by_name(
        self, db: AsyncSession, name: str
    ) -> Optional[RoomType]:
        statement = select(self.model).where(self.model.name == name)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_uid(
        self, db: AsyncSession, uid: UUID
    ) -> Optional[RoomType]:
        statement = select(self.model).options(joinedload(self.model.rooms))
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_multi(
        self, db: AsyncSession, offset: int = 0, limit: int = 20
    ):
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
            items=[r["RoomType"] for r in rows],
        )


room_type_crud = RoomTypeCRUD(RoomType)
