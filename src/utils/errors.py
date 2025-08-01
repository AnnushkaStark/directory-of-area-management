import enum
from typing import Optional

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Error(BaseModel):
    detail: str


class ErrorCodes(enum.Enum):
    # auth
    EMAIL_NOT_FOUND = "Email not found"
    EMAIL_ALREADY_REGISTERED = "Email alredy registered"
    PASSWORDS_DONT_MATCH = "Psswords don`t match"
    INVALID_PASSWORD = "Invalid password"

    # room_type
    ROOM_TYPE_ALREADY_EXISTS = "Room type already exists"


class DomainError(Exception):
    code: ErrorCodes

    def __init__(self, code: ErrorCodes, message: Optional[str] = None):
        self.code = code
        super().__init__(message)


async def domain_error_exception_handler(request: Request, exc: DomainError):
    ERROR_STATUS_MAP = {
        ErrorCodes.ROOM_TYPE_ALREADY_EXISTS: 400,
        ErrorCodes.EMAIL_ALREADY_REGISTERED: 409,
        ErrorCodes.EMAIL_NOT_FOUND: 404,
        ErrorCodes.PASSWORDS_DONT_MATCH: 400,
        ErrorCodes.INVALID_PASSWORD: 400,
    }

    status_code = ERROR_STATUS_MAP.get(exc.code, 500)

    return JSONResponse(
        status_code=status_code,
        content={"message": exc.code.value},
    )


class BaseError(BaseModel):
    message: str


def create_response_schema(description: str):
    return dict(
        model=BaseError,
        description=description,
    )


def _format_description(codes) -> str:
    return "".join(f"<br />{code.value}" for code in codes)[len("<br />") :]


def errs(**_codes):
    ret = dict()
    processed = set()

    for status_codes, codes in _codes.items():
        if not hasattr(codes, "__iter__"):
            codes = (codes,)

        if set(codes) & processed:
            raise RuntimeError("Error codes duplicated")

        processed |= set(codes)

        status_code = int(status_codes.strip("e"))

        ret[status_code] = dict(
            model=BaseError,
            description=_format_description(codes),
        )
    return ret
