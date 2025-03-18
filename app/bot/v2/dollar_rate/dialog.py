from aiogram_dialog import Dialog

from app.bot.v2.dollar_rate.windows import (
    get_dollar_rate_history_window,
    get_main_window,
    get_registry_window,
)

dollar_rate_dialog = Dialog(
    get_main_window(),
    get_dollar_rate_history_window(),
    get_registry_window(),
)
