"""Описание таблиц БД"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base, bigint


class User(Base):
    """Telegram пользователи."""

    telegram_id: Mapped[bigint] = mapped_column(unique=True)
    full_name: Mapped[str | None] = mapped_column(String(120))
    is_subscribe: Mapped[bool] = mapped_column(default=False)

    histories: Mapped[list["DollarHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete, delete-orphan",
        lazy="selectin",
    )


class DollarHistory(Base):
    """История запросов пользователей на получение курса доллара"""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date_time: Mapped[datetime] = mapped_column(DateTime)
    cost_value: Mapped[float]

    user: Mapped["User"] = relationship(back_populates="histories")
