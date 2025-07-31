from sqlalchemy.ext.asyncio import AsyncSession

from crud.account import account_crud
from models import Account
from schemas.account import AccountBase, AccountCreateDB


async def create(
    db: AsyncSession, create_schema: AccountBase, user_id: int
) -> Account:
    create_data = AccountCreateDB(
        **create_schema.model_dump(), user_id=user_id
    )
    await account_crud.create(db=db, create_schema=create_data)


async def update(
    db: AsyncSession, user_id: int, update_data: AccountBase
) -> Account:
    found_account = await account_crud.get_by_user_id(db=db, user_id=user_id)
    return await account_crud.update(
        db=db,
        db_obj=found_account,
        update_data=update_data.model_dump(exclude_unset=True),
    )
