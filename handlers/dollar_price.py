"""Значение курса доллара (в рублях)"""

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from api_requests import DollarConverter
from database import UserCrud
from filters import IsUserCommand


router: Router = Router()


async def show_dollar_rate(info: Message | CallbackQuery) -> None:
    dollar_price: float = await DollarConverter.get_price()
    await UserCrud.save_dollar_price(info.from_user.id, dollar_price)
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
