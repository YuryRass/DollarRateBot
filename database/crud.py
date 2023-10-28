from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users, DollarHistory
from database import async_session


class BaseCrud:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        async with async_session() as session:
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def add(cls, object: Users):
        session: AsyncSession
        async with async_session() as session:
            session.add(object)
            await session.commit()


class UserCrud(BaseCrud):
    model = Users

    @classmethod
    async def is_user_exist(cls, user_tg_id: int) -> bool:
        user: Users | None = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        return user is not None

    @classmethod
    async def is_user_registered(cls, user_tg_id: int) -> bool:
        user: Users = \
            await cls.find_one_or_none(
                telegram_id=user_tg_id
            )
        return user.full_name is not None

    @classmethod
    async def add_user(cls, user_tg_id: int) -> None:
        if not await cls.is_user_exist(user_tg_id):
            user: Users = Users(telegram_id=user_tg_id)
            await cls.add(user)

    @classmethod
    async def add_user_fullname(cls, user_tg_id: int, full_name: str) -> None:
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = full_name
        await cls.add(user)

    @classmethod
    async def save_dollar_price(
        cls, user_tg_id: int, dollar_price: float
    ) -> None:
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
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)

        return user.histories

    @classmethod
    async def add_subscription(
        cls, user_tg_id: int, is_subscribe: bool = True
    ) -> None:
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.is_subscribe = is_subscribe

        await cls.add(user)

    @classmethod
    async def is_user_subscribed(cls, user_tg_id: int) -> bool:
        user: Users | None = \
            await cls.find_one_or_none(
                telegram_id=user_tg_id,
                is_subscribe=True
            )
        return user is not None

    @classmethod
    async def delete_account(cls, user_tg_id: int) -> None:
        user: Users = \
            await cls.find_one_or_none(telegram_id=user_tg_id)
        user.full_name = None
        user.is_subscribe = False

        await cls.add(user)
