from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from api_requests.request import DollarConverter
from filters import IsUserCommand


router: Router = Router()


async def show_dollar_rate(message: Message) -> None:
    dollar_price: str = DollarConverter.get_price()
    await message.answer(
        text=f'Курс доллара: {dollar_price} руб.'
    )


@router.message(Command(commands='dollar'), StateFilter(default_state))
async def get_dollar_price_command(message: Message):
    await show_dollar_rate(message)


@router.callback_query(
    IsUserCommand(command='dollar'), StateFilter(default_state)
)
async def get_dollar_price(callback: CallbackQuery):
    await callback.answer()
    await show_dollar_rate(callback.message)
