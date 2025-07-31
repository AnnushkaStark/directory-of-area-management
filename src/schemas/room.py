from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.room_type import RoomTypeResponse
from schemas.user import UserResponse


class RoomBase(BaseModel):
    name: str = Field(max_length=100)
    area: float
    floor_number: int
    room_number: int


class RoomCreate(RoomBase):
    type_id: int
    users_ids: List[int] = []


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(max_length=100, default=None)
    area: Optional[float] = None
    floor_number: Optional[int] = None
    room_number: Optional[int] = None
    type_id: Optional[int] = None
    users_ids: List[int] = []


class RoomResponse(RoomBase):
    uid: UUID


class RoomFullResponse(RoomBase):
    uid: UUID
    room_type: RoomTypeResponse
    users: List[UserResponse] = []
