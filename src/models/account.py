import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .user import User


class Account(Base):
    """
    Модель аккаунта

    ## Attrs:

        - id: int - идентификатор
        - uid: UUID - идентификатор
        - first_name: str - имя
        - last_name: str - фамилия
        - specialization: str - специализация
        - work_schedule: str (Text) - расписание
        - user_id: int - идентификатор пользователя
          которому принадлежит аккаунт (FK User)
        - user: User - связь с пользователем
    """

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    specialization: Mapped[str] = mapped_column(String, nullable=True)
    work_schedule: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["User"] = relationship("User", back_populates="account")
