from unittest.mock import AsyncMock, patch

import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import SendMessage

from app.api_requests.request import DollarConverter
from app.bot.v1.init_dp.routers import get_routers
from app.database.database import Base
from tests.bot.mocked_aiogram import MockedBot, MockedSession
from tests.bot.v1.database import test_async_engine, test_scoped_session
from tests.bot.v1.factories import DollarHistoryFactory, UserFactory
from tests.bot.v1.helper import DOLLAR_IN_RUB


@pytest.fixture(autouse=True)
def mock_db_session():
    with patch("app.database.database.async_session", new=test_scoped_session):
        yield


@pytest.fixture
def dollar_in_rub() -> float:
    return DOLLAR_IN_RUB


@pytest.fixture(autouse=True)
def mock_dollar_price(dollar_in_rub: float):
    with patch.object(
        DollarConverter, "get_price", new_callable=AsyncMock
    ) as mock_method:
        mock_method.return_value = dollar_in_rub
        yield


@pytest.fixture(autouse=True)
async def create_tables():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def registered_user() -> None:
    async with test_scoped_session() as db:
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


@pytest.fixture
def mock_bot_with_message(bot: MockedBot) -> MockedBot:
    bot.add_result_for(method=SendMessage, ok=True)
    return bot
