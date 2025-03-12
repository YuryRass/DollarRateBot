"""Модуль для создания ассинхронного подключения к БД"""

from functools import wraps

from sqlalchemy import BigInteger, Integer, text
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncEngine,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from typing_extensions import Annotated, Optional

from config import settings

bigint = Annotated[int, "bigint"]


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    type_annotation_map = {bigint: BigInteger()}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as exc:
                await session.rollback()
                raise exc
            finally:
                await session.close()

    return wrapper


async def create_tables() -> None:
    """Создание таблиц БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
