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
                InlineKeyboardButton(
                    text='▶️',
                    callback_data=f'paginator_{paginator + 1}'
                ),
                width=1
            )
        elif len(histories) > PAGINATOR * (paginator + 1):
            kb_builder.row(
                InlineKeyboardButton(
                    text='◀️',
                    callback_data=f'paginator_{paginator - 1}'
                ),
                InlineKeyboardButton(
                    text='▶️',
                    callback_data=f'paginator_{paginator + 1}'
                ),
                width=2
            )
        else:
            kb_builder.row(
                InlineKeyboardButton(
                    text='◀️',
                    callback_data=f'paginator_{paginator - 1}'
                ),
                width=1
            )

    return kb_builder.as_markup()
