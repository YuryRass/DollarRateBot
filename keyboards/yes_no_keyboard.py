"""Клавиатура | Да | Нет |"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_yes_no_keyboard(prefix: str = '') -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с ответами пользователя |Да|Нет|

    Args:
        prefix (str, optional): префикс для callback-а.
    Defaults to ''.

    Returns:
        InlineKeyboardMarkup
    """
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=description,
            callback_data=button
        )
        for button, description
        in {f'{prefix}yes': 'Да', f'{prefix}no': 'Нет'}.items()
    ]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
