from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    specialization: Optional[str] = Field(max_length=100, default=None)
    work_schedule: Optional[str] = Field(max_length=5000, default=None)


class AccountCreateDB(AccountBase):
    user_id: int


class AccountResponse(AccountBase):
    uid: UUID
