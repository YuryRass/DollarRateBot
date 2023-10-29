"""Инициализация главного роутера (диспетчера)"""

from aiogram import Dispatcher

import handlers.other_handlers as other_hdrs
import handlers.dollar_price as dollar_hdr
import handlers.registry_user as reg_hdr
import handlers.user_history as history_hdr
import handlers.user_subscription as subscr_hdr
import handlers.cancel_subscription as cancel_hdr
import handlers.delete_account as del_account_hdr


dispatcher: Dispatcher = Dispatcher()


dispatcher.include_router(other_hdrs.router)
dispatcher.include_router(dollar_hdr.router)
dispatcher.include_router(reg_hdr.router)
dispatcher.include_router(history_hdr.router)
dispatcher.include_router(subscr_hdr.router)
dispatcher.include_router(cancel_hdr.router)
dispatcher.include_router(del_account_hdr.router)
