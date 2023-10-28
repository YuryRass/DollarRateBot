from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_yes_no_keyboard() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=description,
            callback_data=button
        )
        for button, description in {'yes': 'Да', 'no': 'Нет'}.items()
    ]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
