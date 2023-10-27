from datetime import datetime
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, engine
from database.models import Users, DollarHistory
from database import async_session


async def create_tables() -> None:
    """Создание таблиц БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def is_user_exist(user_tg_id: int) -> bool:
    query = select(Users).where(Users.telegram_id == user_tg_id)
    session: AsyncSession
    async with async_session() as session:
        res = await session.execute(query)
        return res.scalar() is not None


async def is_user_registered(user_tg_id: int) -> bool:
    registered_user_query = (
        select(Users).
        where(
            and_(
                Users.telegram_id == user_tg_id,
                Users.full_name.is_not(None)
            )
        )
    )
    session: AsyncSession
    async with async_session() as session:
        res = await session.execute(registered_user_query)
        return res.scalar_one_or_none()


async def add_user(user_tg_id: int) -> None:
    if not await is_user_exist(user_tg_id):
        user: Users = Users(telegram_id=user_tg_id)
        session: AsyncSession
        async with async_session() as session:
            session.add(user)
            await session.commit()


async def add_user_fullname(user_tg_id: int, full_name: str) -> None:

    user_query = (
        select(Users).
        where(Users.telegram_id == user_tg_id)
    )
    session: AsyncSession
    async with async_session() as session:
        res = await session.execute(user_query)
        user: Users = res.scalar_one()
        user.full_name = full_name
        await session.commit()


async def save_dollar_price(user_tg_id: int, dollar_price: float):
    user_query = (
        select(Users).
        where(Users.telegram_id == user_tg_id)
    )
    session: AsyncSession
    async with async_session() as session:
        res = await session.execute(user_query)
        user: Users = res.scalar_one()
        history: DollarHistory = DollarHistory(
            date_time=datetime.now(),
            cost_value=dollar_price
        )
        user.histories.append(history)
        await session.commit()


async def get_user_history(user_tg_id: int) -> list[DollarHistory]:
    query = (
        select(Users).
        where(Users.telegram_id == user_tg_id)
    )
    session: AsyncSession
    async with async_session() as session:
        res = await session.execute(query)
        user: Users = res.scalar_one()
        return user.histories
