"""Регистрация пользователя"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message

from bot.v1.filters.filters import IsUserCommand
from bot.v1.utils.checker_fio import is_correct_fullname
from services.user import UserService

router: Router = Router()


class UserStates(StatesGroup):
    full_name = State()


async def _user_register(info: Message | CallbackQuery, state: FSMContext):
    user_reg: bool = await UserService.is_user_registered(info.from_user.id)
    if isinstance(info, CallbackQuery):
        info = info.message
    if user_reg:
        await info.answer(
            text="Вы уже зарегистрированы!",
        )
    else:
        await info.answer(
            text=("Для регистрации введите свои ФИО\n" "Например: Иванов Иван Иванович")
        )
        await state.set_state(state=UserStates.full_name)


@router.message(Command(commands="register"), StateFilter(default_state))
async def user_register_command(message: Message, state: FSMContext):
    await _user_register(message, state)


@router.callback_query(IsUserCommand(command="register"), StateFilter(default_state))
async def user_registry(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _user_register(callback, state)


@router.message(StateFilter(UserStates.full_name))
async def input_full_name(message: Message, state: FSMContext):
    full_name: str = message.text
    if is_correct_fullname(full_name):
        await UserService.add_user_fullname(message.from_user.id, full_name)
        await message.answer(
            text=(
                "Поздравляю! Теперь Вы зарегестрированы и "
                "можете оформить подписку, чтобы получать оповещения о курсе "
                "доллара каждый день - /subscribe"
            )
        )
    else:
        await message.answer(
            text="ФИО введены некорректно! Попробуйте еще раз /register",
        )
    await state.clear()
