import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .room import Room


class RoomType(Base):
    """
    Модель типа помещения

    ## Attrs
       - id : int - идентификатор
       - uid: UUID - идентификатор
       - name: str - название
       - rooms: List[Room] - список помещений
        относящихся к этому типу
    """

    __tablename__ = "room_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="room_type"
    )
