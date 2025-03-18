"""Инициализация главного роутера (диспетчера)"""

from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from app.bot.v2.dollar_rate.dialog import dollar_rate_dialog
from app.bot.v2.dollar_rate.handlers.handlers import router as start_router

dispatcher: Dispatcher = Dispatcher()

dispatcher.include_router(start_router)
dispatcher.include_router(dollar_rate_dialog)
setup_dialogs(dispatcher)
