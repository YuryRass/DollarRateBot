"""Инициализация главного роутера (диспетчера)"""

from aiogram import Dispatcher

from app.bot.v1.init_dp.routers import get_routers

dispatcher: Dispatcher = Dispatcher()

dispatcher.include_routers(*get_routers())
