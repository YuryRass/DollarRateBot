"""Telegram DollarRateBot"""

import asyncio
import logging

from aiogram import Bot
from aiogram.client.telegram import TelegramAPIServer

from bot.v1.init_dp import dispatcher
from bot.v1.utils.main_menu import set_main_menu
from config import settings
from database.database import create_tables


async def main():
    # Логгирование
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # Создание таблиц, если БД пустая
    await create_tables()

    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        parse_mode='HTML'
    )
    # Если указан адрес в переменной CUSTOM_BOT_API в файле .env,
    # то запускаем Local Telegram API Server
    if settings.CUSTOM_BOT_API:
        bot.session.api = TelegramAPIServer.from_base(
            settings.CUSTOM_BOT_API, is_local=True
        )

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    dispatcher.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
