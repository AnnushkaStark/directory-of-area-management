from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class RoomTypeBase(BaseModel):
    name: str = Field(max_length=100)

    @model_validator(mode="after")
    def name_upper(self):
        self.name = self.name.upper()
        return self


class RoomTypeResponse(RoomTypeBase):
    id: int
    uid: UUID
