"""Запрос к публичному API для получения курса доллара"""
import requests
from requests import Response
from config import settings


class DollarConverter:
    """Курс доллара"""
    @staticmethod
    def get_price() -> str:
        """Возвращает курс доллара в рублях

        Returns:
            str: число рублей
        """
        payload: dict[str, str] = {'fsym': 'USD', 'tsyms': 'RUB'}
        response: Response = requests.get(
            url=settings.URL, params=payload
        )
        price = response.json()
        return price['RUB']
