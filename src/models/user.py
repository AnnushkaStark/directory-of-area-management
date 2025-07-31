import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import RoomUsers

if TYPE_CHECKING:
    from .account import Account
    from .room import Room


class User(Base):
    """
    Модель пользователя

    ## Attrs:
       - id: int - идентификатор
       - uid: UUID - идентификатор
       - email: str - электорнная почта пользователя
       - password: str - хэш пароля пользователя
       - account: Account - связь с аккаутном
       - rooms: List[Room] - связь с помещениями в которых
         может работать пользователь
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    account: Mapped["Account"] = relationship("Account", back_populates="user")
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="users", secondary=RoomUsers.__table__
    )
