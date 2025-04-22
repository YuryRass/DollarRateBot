import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update

from tests.bot.mocked_aiogram import MockedBot
from tests.bot.v1.helper import (
    create_tg_callback,
    create_tg_command_message,
)


@pytest.mark.asyncio
async def test_dollar_price_command(
    dp: Dispatcher,
    mock_bot_with_message: MockedBot,
    dollar_in_rub: float,
    registered_user,
) -> None:
    assert not mock_bot_with_message.session.requests
    message = create_tg_command_message("/dollar")

    result = await dp.feed_update(
        mock_bot_with_message, Update(message=message, update_id=1)
    )
    assert result is not UNHANDLED
    outgoing_message: TelegramType = mock_bot_with_message.get_request()
    assert isinstance(outgoing_message, SendMessage)

    expected_text = f"Курс доллара: {dollar_in_rub} руб."
    assert outgoing_message.text == expected_text


@pytest.mark.asyncio
async def test_dollar_price_callback(
    dp: Dispatcher,
    bot: MockedBot,
    dollar_in_rub: float,
    registered_user,
):
    assert not bot.session.requests
    bot.add_result_for(
        method=AnswerCallbackQuery,
        ok=True,
    )
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )

    # Отправка колбэка с data = dollar
    update = await dp.feed_update(
        bot=bot,
        update=Update(
            callback_query=create_tg_callback("dollar"),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED
    outgoing_callback: TelegramType = bot.get_request()

    assert isinstance(outgoing_callback, SendMessage)
    assert outgoing_callback.text == f"Курс доллара: {dollar_in_rub} руб."
