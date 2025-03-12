"""История пользовательских запросов о курсах доллара"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.v1.filters.filters import IsNotCallBack, IsPaginatorBtn, IsUserCommand
from bot.v1.keyboards import get_history_keyboard
from database.models import DollarHistory
from services.user import UserService

router: Router = Router()


async def _get_user_history(info: Message | CallbackQuery):
    histories: list[DollarHistory] = await UserService.get_user_history(
        info.from_user.id
    )

    history_kb: InlineKeyboardMarkup = get_history_keyboard(histories)

    if isinstance(info, CallbackQuery):
        info = info.message

    await info.answer(
        text="История запросов",
        reply_markup=history_kb,
    )


@router.message(Command(commands="history"), StateFilter(default_state))
async def show_user_history_command(message: Message):
    await _get_user_history(message)


@router.callback_query(IsUserCommand("history"), StateFilter(default_state))
async def show_user_history(callback: CallbackQuery):
    await _get_user_history(callback)


@router.callback_query(IsPaginatorBtn())
async def paginate_pages(callback: CallbackQuery, paginator: int):
    histories: list[DollarHistory] = await UserService.get_user_history(
        callback.from_user.id
    )

    history_kb: InlineKeyboardMarkup = get_history_keyboard(histories, paginator)

    await callback.message.edit_text(
        text="История запросов",
        reply_markup=history_kb,
    )


@router.callback_query(IsNotCallBack())
async def not_call(callback: CallbackQuery):
    await callback.answer()
