import asyncio

import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.v1.init_dp.routers import get_routers
from app.database.database import Base
from tests.bot.mocked_aiogram import MockedBot, MockedSession
from tests.bot.v1.database import async_engine, scoped_session
from tests.bot.v1.factories import DollarHistoryFactory, UserFactory


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Создает экземпляр стандартного цикла событий
    для каждого тестового случая.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
async def registered_user() -> None:
    async with scoped_session() as db:
        user = UserFactory(
            full_name="Иванов Иван Иванович",
            histories=DollarHistoryFactory.create_batch(3),
        )
        db.add(user)
        await db.commit()


@pytest.fixture(scope="session")
def dp() -> Dispatcher:
    disp = Dispatcher(storage=MemoryStorage())
    disp.include_routers(*get_routers())
    return disp


@pytest.fixture(scope="session")
def bot() -> MockedBot:
    bot = MockedBot()
    bot.session = MockedSession()
    return bot
