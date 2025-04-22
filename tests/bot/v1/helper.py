from datetime import datetime

from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Chat, Message, User

from app.bot.v1.lexicon.lexicon import LEXICON

DOLLAR_IN_RUB = 75.0
USER_TG_ID = 1234567
CHAT_ID = 1234567


def create_tg_command_message(command: str) -> Message:
    chat = Chat(id=USER_TG_ID, type=ChatType.PRIVATE)
    user = User(id=USER_TG_ID, is_bot=False, first_name="User")
    return Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text=command,
        date=datetime.now(),
    )


def create_tg_callback(callback_data: str) -> CallbackQuery:
    return CallbackQuery(
        id="chosen",
        chat_instance="test",
        from_user=User(id=USER_TG_ID, is_bot=False, first_name="User"),
        data=callback_data,
        message=Message(
            message_id=42,
            date=datetime.now(),
            text=LEXICON[callback_data],
            chat=Chat(id=USER_TG_ID, type=ChatType.PRIVATE),
        ),
    )


class MockDollarConverter:
    """Мок-класс для тестирования DollarConverter"""

    @staticmethod
    async def get_price() -> float:
        """Возвращает фиксированное значение курса доллара"""
        return DOLLAR_IN_RUB
