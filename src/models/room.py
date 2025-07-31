import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import RoomUsers

if TYPE_CHECKING:
    from .room_type import RoomType
    from .user import User


class Room(Base):
    """
    Модель помещения

    ## Attrs:
       - id: int - идентификатор
       - uid: UUID - идентификатор
       - floor_number: int - номер этажа
       - room_nubmer: int - номер помещения
       - area: float - площадь помещения
       - type_id: int - идентифкатор типа помещения
        FK RoomType
       - room_type: RoomType - связь с типом помещения
       - users: List[User] - список пользователей
        работающих в этом помещении
    """

    __tablename__ = "room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str]
    floor_number: Mapped[int]
    room_number: Mapped[int]
    area: Mapped[float]
    type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("room_type.id", ondelete="CASCADE"), unique=True
    )
    room_type: Mapped["RoomType"] = relationship(
        "RoomType", back_populates="rooms"
    )
    users = Mapped[List["User"]] = relationship(
        "User", back_populates="rooms", secondary=RoomUsers.__table__
    )
