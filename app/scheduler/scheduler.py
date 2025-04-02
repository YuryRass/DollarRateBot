from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config.config import settings

scheduler = AsyncIOScheduler(
    jobstores={"default": SQLAlchemyJobStore(url=settings.STORE_URL)}
)
