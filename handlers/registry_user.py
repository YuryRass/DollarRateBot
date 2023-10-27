from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from filters import IsUserCommand
from database.crud import is_user_registered, add_user_fullname
from utils.checker_fio import is_correct_fullname


router: Router = Router()


class UserStates(StatesGroup):
    full_name = State()


async def _user_registry(message: Message, state: FSMContext):
    user_reg: bool = await is_user_registered(message.from_user.id)
    if user_reg:
        await message.answer(
            text='Вы уже зарегистрированы!',
        )
    else:
        await message.answer(
            text='Для регистрации введите свои ФИО\n' +
            'Например: Иванов Иван Иванович',
        )
        await state.set_state(state=UserStates.full_name)


@router.message(Command(commands='registry'), StateFilter(default_state))
async def user_registry_command(message: Message, state: FSMContext):
    await _user_registry(message, state)


@router.callback_query(
    IsUserCommand(command='registry'), StateFilter(default_state)
)
async def user_registry(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _user_registry(callback.message, state)


@router.message(StateFilter(UserStates.full_name))
async def input_full_name(message: Message, state: FSMContext):
    full_name: str = message.text
    if is_correct_fullname(full_name):
        await add_user_fullname(message.from_user.id, full_name)
        await message.answer(
            text='Поздравляю! Теперь Вы зарегестрированы и ' +
            'можете получать значения курса доллара с выбранной периодичностью'
        )
    else:
        await message.answer(
            text='ФИО введены некорректно! Попробуйте еще раз /registry',
        )
    await state.clear()
