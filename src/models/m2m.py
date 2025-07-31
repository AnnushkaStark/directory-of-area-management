from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from databases.database import Base


class RoomUsers(Base):
    """
    Модель связи m2m (помещение - пользователь)

    ## Attrs:
      - user_id: int - идетификатор пользователя
      - room_id: int - идентификатор помещения

    """

    __tablename__ = "room_users"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("room.id", ondelete="CASCADE"),
        primary_key=True,
    )
