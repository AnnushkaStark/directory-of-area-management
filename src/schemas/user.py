from uuid import UUID

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from schemas.account import AccountResponse


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    password_confirm: str

    @validator("email")
    def email_check(cls, v: EmailStr) -> EmailStr:
        email_info = validate_email(v, check_deliverability=True)
        email = email_info.normalized
        return email


class UserCreateDB(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    uid: UUID
    email: str


class UserFullResponse(UserResponse):
    account: AccountResponse
