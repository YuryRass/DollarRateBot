from datetime import datetime

from aiogram.enums import ChatType
from aiogram.types import Chat, Message, User


def create_tg_command_message(command: str, user_id: int) -> Message:
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=user_id, is_bot=False, first_name="User")
    return Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text=command,
        date=datetime.now(),
    )
