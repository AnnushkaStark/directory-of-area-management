from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Account
from schemas.account import AccountBase, AccountResponse

from .async_crud import BaseAsyncCRUD


class AccountCRUD(BaseAsyncCRUD[Account, AccountBase, AccountResponse]):
    async def get_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> Optional[Account]:
        statament = select(self.model).where(self.model.user_id == user_id)
        result = await db.execute(statament)
        return result.scalars().first()


account_crud = AccountCRUD(Account)
