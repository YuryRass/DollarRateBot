"""Модуль настроек"""

from typing import Literal

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Данные, считывающиеся из файла .env"""

    BOT_VERSION: Literal["1", "2"]
    BOT_TOKEN: str
    PAYMENTS_TOKEN: str
    URL: HttpUrl  # адрес API с курсом валют

    # PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # http://localhost:8081
    CUSTOM_BOT_API: str | None
    URL_WEBHOOK: str

    @property
    def DATABASE_URL(self):
        """Адрес PostgreSQL базы данных"""

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
