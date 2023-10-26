from database import Base, engine
from database.models import Users, DollarHistory


async def create_tables() -> None:
    """Создание таблиц БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
