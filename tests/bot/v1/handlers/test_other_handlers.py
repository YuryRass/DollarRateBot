import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update

from app.bot.v1.keyboards.main_keyboard import get_main_keyboard
from app.bot.v1.lexicon.lexicon import LEXICON, START_MESSAGE
from app.services.user import UserService
from tests.bot.mocked_aiogram import MockedBot
from tests.bot.v1.helper import create_tg_command_message


@pytest.mark.parametrize("tg_command", ["/help", "/start"])
@pytest.mark.asyncio
async def test_basic_commands(
    tg_command: str, dp: Dispatcher, mock_bot_with_message: MockedBot
) -> None:
    # assert not mock_bot_with_message.session.requests
    message = create_tg_command_message(tg_command)

    # пользователь не зареган
    assert not await UserService.is_user_registered(user_tg_id=message.from_user.id)

    result = await dp.feed_update(mock_bot_with_message, Update(message=message, update_id=1))
    assert result is not UNHANDLED
    outgoing_message: TelegramType = mock_bot_with_message.get_request()
    assert isinstance(outgoing_message, SendMessage)

    expected_text = (
        START_MESSAGE.format(
            user_full_name=message.from_user.full_name, msg=LEXICON[tg_command]
        )
        if tg_command == "/start"
        else LEXICON[tg_command]
    )
    assert outgoing_message.text == expected_text


@pytest.mark.asyncio
async def test_start_command_for_registered_user(
    registered_user, dp: Dispatcher, mock_bot_with_message: MockedBot
) -> None:
    # assert not mock_bot_with_message.session.requests
    message = create_tg_command_message("/start")

    # пользователь зареган
    assert await UserService.is_user_registered(user_tg_id=message.from_user.id)

    result = await dp.feed_update(mock_bot_with_message, Update(message=message, update_id=1))
    assert result is not UNHANDLED
    outgoing_message: TelegramType = mock_bot_with_message.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == (
        START_MESSAGE.format(
            user_full_name=message.from_user.full_name,
            msg=LEXICON["/start"],
        )
    )
    assert outgoing_message.reply_markup == get_main_keyboard("register")
