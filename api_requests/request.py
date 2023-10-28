"""Запрос к публичному API для получения курса доллара"""
from aiohttp import ClientSession
from config import settings


class DollarConverter:
    """Курс доллара"""

    @staticmethod
    async def get_price() -> float:
        payload: dict[str, str] = {'fsym': 'USD', 'tsyms': 'RUB'}
        async with ClientSession() as session:
            async with session.get(
                url=str(settings.URL),
                params=payload,
            ) as response:
                price = await response.json()
                return float(price['RUB'])
