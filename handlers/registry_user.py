"""Регистрация пользователя"""

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from filters import IsUserCommand
from database import UserCrud
from utils.checker_fio import is_correct_fullname


router: Router = Router()


class UserStates(StatesGroup):
    full_name = State()


async def _user_register(info: Message | CallbackQuery, state: FSMContext):
    user_reg: bool = await UserCrud.is_user_registered(info.from_user.id)
    if isinstance(info, CallbackQuery):
        info = info.message
    if user_reg:
        await info.answer(
            text='Вы уже зарегистрированы!',
        )
    else:
        await info.answer(
            text='Для регистрации введите свои ФИО\n' +
            'Например: Иванов Иван Иванович',
        )
        await state.set_state(state=UserStates.full_name)


@router.message(Command(commands='register'), StateFilter(default_state))
async def user_register_command(message: Message, state: FSMContext):
    await _user_register(message, state)


@router.callback_query(
    IsUserCommand(command='register'), StateFilter(default_state)
)
async def user_registry(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _user_register(callback, state)


@router.message(StateFilter(UserStates.full_name))
async def input_full_name(message: Message, state: FSMContext):
    full_name: str = message.text
    if is_correct_fullname(full_name):
        await UserCrud.add_user_fullname(message.from_user.id, full_name)
        await message.answer(
            text='Поздравляю! Теперь Вы зарегестрированы и ' +
            'можете оформить подписку, чтобы получать оповещения о курсе ' +
            'доллара каждый день - /subscribe'
        )
    else:
        await message.answer(
            text='ФИО введены некорректно! Попробуйте еще раз /register',
        )
    await state.clear()
