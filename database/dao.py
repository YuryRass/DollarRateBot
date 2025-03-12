"""Create Read Update Delete"""

from datetime import datetime
from typing import Any, Generic, Type, TypeVar

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Base
from database.models import DollarHistory, User

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """Базовый класс основных операций для БД."""

    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def find_one_or_none(self, **kwargs: Any):
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Запись {self.model.__name__} по параметрам {kwargs} {'найдена' if record else 'не найдена'}."
            logger.info(log_message)
            return record
        except SQLAlchemyError as exc:
            logger.error(f"Ошибка при поиске записи по параметрам {kwargs}: {exc}")
            raise

    async def add(self, object: Any):
        """Добавляет объект в модель."""
        self._session.add(object)
        await self._session.commit()


class UserDAO(BaseDAO[User]):
    """Операции для модели User."""

    model = User

    async def is_user_exist(self, user_tg_id: int) -> bool:
        """
        Проверка на существование пользователя в модели.

        Args:
            user_tg_id (int): Telegram ID пользователя

        Returns:
            bool: True, если пользователь существует
        """
        user: User | None = await self.find_one_or_none(telegram_id=user_tg_id)
        return user is not None

    async def is_user_registered(self, user_tg_id: int) -> bool:
        """
        Проверяет зареган ли Tg пользователь.

        Args:
            user_tg_id (int): Telegram ID пользователя

        Returns:
            bool: True, если зареган
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)
        return user.full_name is not None

    async def add_user(self, user_tg_id: int) -> None:
        """
        Добавление пользователя в таблицу.

        Args:
            user_tg_id (int): Telegram ID пользователя
        """
        if not await self.is_user_exist(user_tg_id):
            user: User = User(telegram_id=user_tg_id)
            await self.add(user)

    async def add_user_fullname(self, user_tg_id: int, full_name: str) -> None:
        """
        Добавляет ФИО пользователя в таблицу после регистрации.

        Args:
            user_tg_id (int): Telegram ID пользователя
            full_name (str): ФИО пользователя
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = full_name
        await self.add(user)

    async def save_dollar_price(self, user_tg_id: int, dollar_price: float) -> None:
        """
        Сохраняет данные о курсе доллара в таблице.

        Args:
            user_tg_id (int): Telegram ID пользователя
            dollar_price (float): цена 1 доллара в рублях
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)
        user.histories.append(
            DollarHistory(date_time=datetime.now(), cost_value=dollar_price)
        )
        await self.add(user)

    async def get_user_history(self, user_tg_id: int) -> list[DollarHistory]:
        """
        Возвращает историю пользовательских запросов о курсе доллара.

        Args:
            user_tg_id (int): Telegram ID пользователя.

        Returns:
            list[DollarHistory]
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)

        return user.histories

    async def add_subscription(self, user_tg_id: int, is_subscribe: bool = True) -> None:
        """
        Изменяет информацию о подписке пользователя.

        Args:
            user_tg_id (int): Telegram ID пользователя
            is_subscribe (bool, optional): есть ли у пользователя подписка.
        Defaults to True.
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)
        user.is_subscribe = is_subscribe

        await self.add(user)

    async def is_user_subscribed(self, user_tg_id: int) -> bool:
        """
        Проверяет есть ли у пользователя подписка на оповещения о курсе доллара.

        Args:
            user_tg_id (int): Telegram ID пользователя
        """
        user: User | None = await self.find_one_or_none(
            telegram_id=user_tg_id, is_subscribe=True
        )
        return user is not None

    async def delete_account(self, user_tg_id: int) -> None:
        """
        Удаляет аккаунт пользователя, т.е. удаляет из таблицы
        его данные о подписке и ФИО

            Args:
                user_tg_id (int): Telegram ID пользователя
        """
        user: User = await self.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = None
        user.is_subscribe = False

        await self.add(user)
