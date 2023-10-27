"""Запрос к публичному API для получения курса доллара"""
import requests
from requests import Response
from config import settings


class DollarConverter:
    """Курс доллара"""
    @staticmethod
    def get_price() -> float:
        """Возвращает курс доллара в рублях

        Returns:
            float: число рублей
        """
        payload: dict[str, str] = {'fsym': 'USD', 'tsyms': 'RUB'}
        response: Response = requests.get(
            url=settings.URL, params=payload
        )
        price = response.json()
        return float(price['RUB'])
