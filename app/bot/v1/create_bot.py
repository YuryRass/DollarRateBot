from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer

from app.config.config import settings

BOT: Bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)
# Если указан адрес в переменной CUSTOM_BOT_API в файле .env,
# то запускаем Local Telegram API Server
if settings.CUSTOM_BOT_API:
    BOT.session.api = TelegramAPIServer.from_base(
        settings.CUSTOM_BOT_API, is_local=True
    )
