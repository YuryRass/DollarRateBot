"""Значение курса доллара (в рублях)"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from bot.v1.filters.filters import IsUserCommand
from services.dollar_rate import DollarRateService

router: Router = Router()


async def show_dollar_rate(info: Message | CallbackQuery) -> None:
    dollar_price = await DollarRateService.get_and_save_dollar_rate(info.from_user.id)
    if isinstance(info, CallbackQuery):
        info = info.message
    await info.answer(text=f"Курс доллара: {dollar_price} руб.")


@router.message(Command(commands="dollar"), StateFilter(default_state))
async def get_dollar_price_command(message: Message):
    await show_dollar_rate(message)


@router.callback_query(IsUserCommand(command="dollar"), StateFilter(default_state))
async def get_dollar_price(callback: CallbackQuery):
    await callback.answer()
    await show_dollar_rate(callback)
