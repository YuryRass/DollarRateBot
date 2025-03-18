from sqlalchemy.ext.asyncio import AsyncSession

from app.api_requests.request import DollarConverter
from app.database.dao import UserDAO
from app.database.database import connection


class DollarRateService:
    """Сервисный слой для курса доллара."""
    @classmethod
    @connection
    async def get_and_save_dollar_rate(cls, user_tg_id: int, session: AsyncSession) -> float:
        dollar_price = await DollarConverter.get_price()
        await UserDAO(session).save_dollar_price(user_tg_id, dollar_price)
        return dollar_price
