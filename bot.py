"""Telegram DollarRateBot"""

import asyncio
from aiogram import Bot

from init_dp import dispatcher
from config import settings
from utils.main_menu import set_main_menu
from database import create_tables


async def main():
    await create_tables()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        parse_mode='HTML'
    )

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    dispatcher.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
