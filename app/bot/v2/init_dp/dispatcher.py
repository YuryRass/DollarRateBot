"""Инициализация главного роутера (диспетчера)"""

from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from app.bot.v2.dollar_rate.dialog import dollar_rate_dialog
from app.bot.v2.dollar_rate.handlers.handlers import router as start_router
from app.bot.v2.nats_storage.storage import NatsStorage


def get_dispatcher(storage: NatsStorage) -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(start_router)
    dispatcher.include_router(dollar_rate_dialog)
    setup_dialogs(dispatcher)

    return dispatcher
