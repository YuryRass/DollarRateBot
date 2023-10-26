import asyncio
from aiogram import Bot, Dispatcher
from handlers.user_handlers import router
from config import settings


async def main():
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        parse_mode='HTML'
    )
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    dp.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
