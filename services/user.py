from sqlalchemy.ext.asyncio import AsyncSession

from database.dao import UserDAO
from database.database import connection
from database.models import DollarHistory, User


class UserService:
    "Сервисный слой для пользователей."

    @classmethod
    @connection
    async def add_user(
        cls,
        user_tg_id: int,
        session: AsyncSession,
    ) -> None:
        user_dao = UserDAO(session)
        if not await user_dao.is_user_exist(user_tg_id=user_tg_id):
            await user_dao.add(User(telegram_id=user_tg_id))

    @classmethod
    @connection
    async def is_user_registered(
        cls,
        user_tg_id: int,
        session: AsyncSession,
    ) -> bool:
        return await UserDAO(session).is_user_registered(user_tg_id)

    @classmethod
    @connection
    async def get_user_history(
        cls,
        user_tg_id: int,
        session: AsyncSession,
    ) -> list[DollarHistory]:
        return await UserDAO(session).get_user_history(user_tg_id)

    @classmethod
    @connection
    async def add_user_fullname(
        cls,
        user_tg_id: int,
        full_name: str,
        session: AsyncSession,
    ) -> None:
        await UserDAO(session).add_user_fullname(user_tg_id, full_name)

    @classmethod
    @connection
    async def delete_account(
        cls,
        user_tg_id: int,
        session: AsyncSession,
    ) -> None:
        await UserDAO(session).delete_account(user_tg_id)

    @classmethod
    @connection
    async def is_user_subscribed(
        cls,
        user_tg_id: int,
        session: AsyncSession,
    ) -> bool:
        return await UserDAO(session).is_user_subscribed(user_tg_id)

    @classmethod
    @connection
    async def add_subscription(cls, user_tg_id, session: AsyncSession) -> None:
        return await UserDAO(session).add_subscription(user_tg_id)

    @classmethod
    @connection
    async def cancel_subscription(cls, user_tg_id, session: AsyncSession) -> None:
        return await UserDAO(session).add_subscription(user_tg_id, False)
