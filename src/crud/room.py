from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from models import Room
from schemas.pagination import PaginationResponse
from schemas.room import RoomCreate, RoomResponse

from .async_crud import BaseAsyncCRUD


class RoomCRUD(BaseAsyncCRUD[Room, RoomCreate, BaseModel]):
    async def get_by_uid(self, db: AsyncSession, uid: UUID) -> Optional[Room]:
        statement = select(self.model).options(
            joinedload(
                self.model.room_type,
            ),
            joinedload(self.model.users),
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_multi(
        self, db: AsyncSession, offset: int = 0, limit: int = 20
    ) -> PaginationResponse[RoomResponse]:
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
            items=[r["Room"] for r in rows],
        )

    async def create(
        self, db: AsyncSession, create_schema: RoomCreate, commit: bool = True
    ) -> Room:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(self.model)
            .options(selectinload(self.model.users))
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_id: int,
        update_data: RoomCreate,
        commit: bool = True,
    ) -> Room:
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)
        if not update_data:
            return self.get_by_id(db=db, obj_id=obj_id)
        stmt = (
            update(self.model)
            .values(**update_data)
            .where(self.model.id == obj_id)
            .options(joinedload(self.model.users))
            .returning(self.model)
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()


room_crud = RoomCRUD(Room)
