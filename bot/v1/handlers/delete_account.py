"""Удаление аккаунта"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message

from bot.v1.filters.filters import IsUserCommand
from bot.v1.keyboards import get_yes_no_keyboard
from services.user import UserService

router: Router = Router()


class UserStates(StatesGroup):
    delete_account = State()


async def _delete_account(info: Message | CallbackQuery, state: FSMContext):
    if isinstance(info, CallbackQuery):
        info = info.message
    await info.answer(
        text="Вы уверены, что хотите удалить свой аккаунт?",
        reply_markup=get_yes_no_keyboard("delete"),
    )
    await state.set_state(state=UserStates.delete_account)


@router.message(Command(commands="unregister"), StateFilter(default_state))
async def delete_account_command(message: Message, state: FSMContext):
    await _delete_account(message, state)


@router.callback_query(IsUserCommand("unregister"), StateFilter(default_state))
async def del_account(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _delete_account(callback, state)


@router.callback_query(
    lambda answer: "delete" in answer.data, StateFilter(UserStates.delete_account)
)
async def delete_user_account(callback: CallbackQuery, state: FSMContext):
    if callback.data.endswith("no"):
        await callback.message.answer(text="Ну и правильно!")
    # yes
    else:
        await UserService.delete_account(callback.from_user.id)
        await callback.message.answer(text="Ваш аккаунт удалён!")
    await state.clear()
