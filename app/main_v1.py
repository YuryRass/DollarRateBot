"""Telegram DollarRateBot"""

from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, Request
from loguru import logger

from app.bot.v1.create_bot import BOT
from app.bot.v1.init_dp import dispatcher
from app.bot.v1.utils.main_menu import set_main_menu
from app.config.config import settings
from app.routers.dollar_rate import router as router_fast_stream

WEBHOOK_PATH = f"/bot/{settings.BOT_TOKEN}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Бот запущен...")
    await set_main_menu(BOT)
    logger.success("Брокер RabbitMQ запущен...")
    webhook_link = f"{settings.URL_WEBHOOK}{WEBHOOK_PATH}"
    await BOT.set_webhook(
        url=webhook_link,
        allowed_updates=dispatcher.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logger.success(f"Вебхук установлен: {settings.URL_WEBHOOK}")
    yield
    logger.info("Бот остановлен...")
    await BOT.delete_webhook()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request) -> None:
    logger.info("Получен запрос с вебхука.")
    try:
        update = Update.model_validate(await request.json(), context={"bot": BOT})
        await dispatcher.feed_update(BOT, update)
        logger.info("Обновление успешно обработано.")
    except Exception as exc:
        logger.error(f"Ошибка при обработке обновления с вебхука: {exc}")

app.include_router(router_fast_stream)
