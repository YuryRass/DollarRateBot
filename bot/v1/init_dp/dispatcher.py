"""Инициализация главного роутера (диспетчера)"""

from aiogram import Dispatcher

import bot.v1.handlers.cancel_subscription as cancel_hdr
import bot.v1.handlers.delete_account as del_account_hdr
import bot.v1.handlers.dollar_price as dollar_hdr
import bot.v1.handlers.other_handlers as other_hdrs
import bot.v1.handlers.registry_user as reg_hdr
import bot.v1.handlers.user_history as history_hdr
import bot.v1.handlers.user_subscription as subscr_hdr

dispatcher: Dispatcher = Dispatcher()


dispatcher.include_router(other_hdrs.router)
dispatcher.include_router(dollar_hdr.router)
dispatcher.include_router(reg_hdr.router)
dispatcher.include_router(history_hdr.router)
dispatcher.include_router(subscr_hdr.router)
dispatcher.include_router(cancel_hdr.router)
dispatcher.include_router(del_account_hdr.router)
