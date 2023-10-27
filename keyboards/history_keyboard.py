from math import ceil
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import DollarHistory

PAGINATOR = 7


def get_history_keyboard(
    histories: list[DollarHistory], paginator: int = 0
) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=f'{it.date_time.strftime("%d.%m.%y %H:%M:%S")}' +
            f' 💵 {it.cost_value} руб.',
            callback_data='not_call',
        )
        for it in histories[PAGINATOR * paginator:PAGINATOR * (paginator + 1)]
    ]

    kb_builder.row(*buttons, width=1)

    if len(histories) > PAGINATOR:
        if paginator == 0:
            kb_builder.row(
                _pages_statistic_btn(len(histories), paginator + 1),
                _paginator_btn('▶️', paginator + 1),
                width=2
            )
        elif len(histories) > PAGINATOR * (paginator + 1):
            kb_builder.row(
                _paginator_btn('◀️', paginator - 1),
                _pages_statistic_btn(len(histories), paginator + 1),
                _paginator_btn('▶️', paginator + 1),
                width=3
            )
        else:
            kb_builder.row(
                _paginator_btn('◀️', paginator - 1),
                _pages_statistic_btn(len(histories), paginator + 1),
                width=2
            )

    return kb_builder.as_markup()


def _paginator_btn(text: str, paginator: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=f'paginator_{paginator}'
    )


def _pages_statistic_btn(
    len_records: int, paginator: int
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=f'{paginator} / ' +
        f'{ceil(len_records / PAGINATOR)}',
        callback_data='not_call'
    )
