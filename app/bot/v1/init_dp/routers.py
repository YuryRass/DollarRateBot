from aiogram import Router

import app.bot.v1.handlers.cancel_subscription as cancel_hdr
import app.bot.v1.handlers.delete_account as del_account_hdr
import app.bot.v1.handlers.dollar_price as dollar_hdr
import app.bot.v1.handlers.other_handlers as other_hdrs
import app.bot.v1.handlers.registry_user as reg_hdr
import app.bot.v1.handlers.user_history as history_hdr
import app.bot.v1.handlers.user_subscription as subscr_hdr


def get_routers() -> list[Router]:
    return [
        other_hdrs.router,
        dollar_hdr.router,
        reg_hdr.router,
        history_hdr.router,
        subscr_hdr.router,
        cancel_hdr.router,
        del_account_hdr.router,
    ]
