from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.v2.dollar_rate.getters import get_dollar_history, get_user_full_name
from app.bot.v2.dollar_rate.handlers.handlers import (
    BUTTON_MAPPER,
    correct_fullname_handler,
    error_fullname_handler,
)
from app.bot.v2.dollar_rate.keyboards import paginated_history
from app.bot.v2.dollar_rate.state import DollarRateState
from app.bot.v2.lexicon.lexicon import LEXICON
from app.bot.v2.utils.checker_fio import check_fullname


def get_main_window() -> Window:
    """Главное окно получения курса доллара."""
    buttons = [
        Button(text=Const(description), id=button, on_click=BUTTON_MAPPER.get(button))
        for button, description in LEXICON.items()
        if not button.startswith("/")
    ]

    return Window(
        Multi(
            Format("<b>Рад Вас видеть, {user_full_name}!</b>"),
            Const(text=LEXICON["/start"]),
            sep="\n\n",
        ),
        Group(
            *buttons,
            width=2,
        ),
        state=DollarRateState.start,
        getter=get_user_full_name,
    )


def get_dollar_rate_history_window() -> Window:
    return Window(
        Format("История запросов ({len_history} записей)"),
        paginated_history(),
        state=DollarRateState.history,
        getter=get_dollar_history,
    )


def get_registry_window() -> Window:
    return Window(
        Const(
            text=("Для регистрации введите свои ФИО\n" "Например: Иванов Иван Иванович")
        ),
        TextInput(
            id="fio_input",
            type_factory=check_fullname,
            on_success=correct_fullname_handler,
            on_error=error_fullname_handler,
        ),
        state=DollarRateState.registry,
    )
