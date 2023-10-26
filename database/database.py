from typing_extensions import Annotated
from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncEngine, async_sessionmaker,
    create_async_engine
)
from config import settings

bigint = Annotated[int, "bigint"]


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=True
)


class Base(DeclarativeBase):
    type_annotation_map = {
        bigint: BigInteger()
    }
