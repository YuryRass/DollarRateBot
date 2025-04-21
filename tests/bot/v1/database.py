import asyncio

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

TEST_DB_URL = "sqlite+aiosqlite:///tests/test_db.sqlite"

test_async_engine = create_async_engine(TEST_DB_URL)
test_async_session = async_sessionmaker(test_async_engine)
test_scoped_session = async_scoped_session(
    test_async_session,
    scopefunc=asyncio.current_task,
)
