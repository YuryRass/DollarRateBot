"""Инлаин клавиатура, отображающаяся при команде /start"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import LEXICON


def get_main_keyboard(extra_btn: str = 'unregistry') -> InlineKeyboardMarkup:
    """Возвращает главную клавиатуру (команда /start)

    Args:
        extra_btn (str, optional): кнопки, которые не должны быть на клаве.
    Defaults to 'unregistry'.

    Returns:
        InlineKeyboardMarkup
    """
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=description,
            callback_data=button
        )
        for button, description in LEXICON.items()
        if not button.startswith('/') and button != extra_btn
    ]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
