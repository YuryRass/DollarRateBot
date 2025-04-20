from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Chat, Message, Update, User

from app.bot.v1.lexicon.lexicon import LEXICON, START_MESSAGE
from app.services.user import UserService
from tests.bot.mocked_aiogram import MockedBot


@pytest.mark.parametrize("tg_command", ["/help", "/start"])
async def test_basic_commands(tg_command: str, dp: Dispatcher, bot: MockedBot) -> None:
    assert not bot.session.requests
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(
        id=1234567,
        is_bot=False,
        first_name="User",
        full_name="User Userov",
    )
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text=tg_command,
        date=datetime.now(),
    )
    # пользователь не зареган
    assert not await UserService.is_user_registered(user_tg_id=message.from_user.id)

    result = await dp.feed_update(bot, Update(message=message, update_id=1))
    assert result is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert (
        outgoing_message.text == (
            START_MESSAGE.format(
                user_full_name=message.from_user.full_name, msg=LEXICON[tg_command]
            )
        )
        if tg_command == "/start"
        else LEXICON[tg_command]
    )
