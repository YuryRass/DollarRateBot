"""Telegram DollarRateBot"""

from contextlib import asynccontextmanager

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import Depends, FastAPI, Request
from loguru import logger

from app.bot.v2.create_bot import BOT
from app.bot.v2.init_dp.dispatcher import get_dispatcher
from app.bot.v2.nats_storage.storage import get_nats_client_and_storage
from app.config.config import rabbit_broker, settings
from app.routers.dollar_rate import router as router_fast_stream
from app.scheduler.scheduler import scheduler

WEBHOOK_PATH = f"/bot/{settings.BOT_TOKEN}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Бот запущен...")
    await rabbit_broker.start()
    scheduler.start()
    logger.success("Брокер RabbitMQ запущен...")
    webhook_link = f"{settings.URL_WEBHOOK}{WEBHOOK_PATH}"

    nats_client, storage = await get_nats_client_and_storage()
    dispatcher = get_dispatcher(storage=storage)
    app.state.dispatcher = dispatcher
    logger.success("Хранилище Nats создано...")

    await BOT.set_webhook(
        url=webhook_link,
        allowed_updates=dispatcher.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logger.success(f"Вебхук установлен: {settings.URL_WEBHOOK}")

    yield
    logger.info("Бот остановлен...")
    await rabbit_broker.close()
    scheduler.shutdown()
    await nats_client.close()
    await BOT.delete_webhook()


app = FastAPI(lifespan=lifespan)


async def get_dp(request: Request):
    return request.app.state.dispatcher


@app.post(WEBHOOK_PATH)
async def webhook(request: Request, dispatcher: Dispatcher = Depends(get_dp)) -> None:
    logger.info("Получен запрос с вебхука.")
    try:
        update = Update.model_validate(await request.json(), context={"bot": BOT})
        await dispatcher.feed_update(BOT, update)
        logger.info("Обновление успешно обработано.")
    except Exception as exc:
        logger.error(f"Ошибка при обработке обновления с вебхука: {exc}")


app.include_router(router_fast_stream)
