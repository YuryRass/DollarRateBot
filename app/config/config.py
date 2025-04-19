"""Модуль настроек"""

from urllib.parse import quote

from faststream.rabbit import RabbitBroker
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Данные, считывающиеся из файла .env"""

    BOT_TOKEN: str
    PAYMENTS_TOKEN: str
    URL: HttpUrl  # адрес API с курсом валют

    # PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # RabbitMQ
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    # Scheduler store
    STORE_URL: str = "sqlite:///data/jobs.sqlite"

    # http://localhost:8081
    CUSTOM_BOT_API: str | None
    URL_WEBHOOK: str
    SHEDULER_SENDING_DOLLAR_RATE_PREFIX: str = "sending_dollar_rate"
    DOLLAR_RATE_QUEUE: str = "q__dollar_rate"

    # NATS key/value
    NATS_SERVERS: str

    @property
    def DATABASE_URL(self):
        """Адрес PostgreSQL базы данных"""

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USERNAME}:{quote(self.RABBITMQ_PASSWORD)}@"
            f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
rabbit_broker = RabbitBroker(url=settings.RABBITMQ_URL)
