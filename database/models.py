"""Описание таблиц БД"""

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, bigint


class Users(Base):
    """Telegram пользователи"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[bigint] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=True)
    is_subscribe: Mapped[bool] = mapped_column(default=False)

    histories: Mapped[list["DollarHistory"]] = relationship(
        back_populates="user", cascade="all, delete, delete-orphan",
        lazy='selectin'
    )


class DollarHistory(Base):
    """История запросов пользователей на получение курса доллара"""

    __tablename__ = 'dollar_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    cost_value: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship(
        back_populates="histories"
    )
