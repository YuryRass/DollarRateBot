import asyncio
from aiogram import Bot, Dispatcher

from config import settings
from utils.main_menu import set_main_menu

import handlers.other_handlers as other_hdrs
import handlers.dollar_price as dollar_hdr
import handlers.registry_user as reg_hdr
import handlers.user_history as history_hdr
import handlers.user_subscription as subscr_hdr

from database.crud import create_tables


async def main():
    await create_tables()
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        parse_mode='HTML'
    )

    dp.include_router(other_hdrs.router)
    dp.include_router(dollar_hdr.router)
    dp.include_router(reg_hdr.router)
    dp.include_router(history_hdr.router)
    dp.include_router(subscr_hdr.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    dp.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
