import asyncio

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

TEST_DB_URL = "sqlite+aiosqlite:///tests/test_db.sqlite"

async_engine = create_async_engine(TEST_DB_URL)
async_session = async_sessionmaker(async_engine)
scoped_session = async_scoped_session(async_session, scopefunc=asyncio.current_task)
