"""Create Read Update Delete"""

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users, DollarHistory
from database import async_session


class BaseCrud:
    """Базовый класс основных операций для БД"""

    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """Возвращает один либо пустой объект модели
        """
        query = select(cls.model).filter_by(**filter_by)
        async with async_session() as session:
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def add(cls, object):
        """Добавляет объект в модель
        """
        session: AsyncSession
        async with async_session() as session:
            session.add(object)
            await session.commit()


class UserCrud(BaseCrud):
    """Операции для модели Users"""

    model = Users

    @classmethod
    async def is_user_exist(cls, user_tg_id: int) -> bool:
        """Проверка на существование пользователя в модели

        Args:
            user_tg_id (int): Telegram ID пользователя

        Returns:
            bool: True, если пользователь существует
        """
        user: Users | None = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        return user is not None

    @classmethod
    async def is_user_registered(cls, user_tg_id: int) -> bool:
        """Проверяет зареган ли Tg пользователь

        Args:
            user_tg_id (int): Telegram ID пользователя

        Returns:
            bool: True, если зареган
        """
        user: Users = \
            await cls.find_one_or_none(
                telegram_id=user_tg_id
            )
        return user.full_name is not None

    @classmethod
    async def add_user(cls, user_tg_id: int) -> None:
        """Добавление пользователя вместе с его Tg ID в таблицу

        Args:
            user_tg_id (int): Telegram ID пользователя
        """
        if not await cls.is_user_exist(user_tg_id):
            user: Users = Users(telegram_id=user_tg_id)
            await cls.add(user)

    @classmethod
    async def add_user_fullname(cls, user_tg_id: int, full_name: str) -> None:
        """Добавляет ФИО пользователя в таблицу

        Args:
            user_tg_id (int): Telegram ID пользователя
            full_name (str): ФИО пользователя
        """
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = full_name
        await cls.add(user)

    @classmethod
    async def save_dollar_price(
        cls, user_tg_id: int, dollar_price: float
    ) -> None:
        """Сохраняет данные о курсе доллара в таблице

        Args:
            user_tg_id (int): Telegram ID пользователя
            dollar_price (float): цена 1 доллара в рублях
        """
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.histories.append(
            DollarHistory(
                date_time=datetime.now(),
                cost_value=dollar_price
            )
        )
        await cls.add(user)

    @classmethod
    async def get_user_history(cls, user_tg_id: int) -> list[DollarHistory]:
        """Возвращает историю пользовательских запросов о курсе доллара

        Args:
            user_tg_id (int): Telegram ID пользователя

        Returns:
            list[DollarHistory]
        """
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)

        return user.histories

    @classmethod
    async def add_subscription(
        cls, user_tg_id: int, is_subscribe: bool = True
    ) -> None:
        """Изменяет информацию о подписке пользователя

        Args:
            user_tg_id (int): Telegram ID пользователя
            is_subscribe (bool, optional): есть ли у пользователя подписка.
        Defaults to True.
        """
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.is_subscribe = is_subscribe

        await cls.add(user)

    @classmethod
    async def is_user_subscribed(cls, user_tg_id: int) -> bool:
        """Проверяет есть ли у пользователя подписка

        Args:
            user_tg_id (int): Telegram ID пользователя

        """
        user: Users | None = \
            await cls.find_one_or_none(
                telegram_id=user_tg_id,
                is_subscribe=True
            )
        return user is not None

    @classmethod
    async def delete_account(cls, user_tg_id: int) -> None:
        """Удаляет аккаунт пользователя, т.е. удаляет из таблицы
    его данные о подписке и ФИО

        Args:
            user_tg_id (int): Telegram ID пользователя
        """
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = None
        user.is_subscribe = False

        await cls.add(user)
