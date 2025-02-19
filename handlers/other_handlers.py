"""Обработка команд /start и /help"""

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state

from lexicon import LEXICON
from keyboards import get_main_keyboard
from database import UserCrud


router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start(message: Message):
    # добавление пользователя, если его нет в таблице
    await UserCrud.add_user(message.from_user.id)

    # главная клавиатура для пользователя
    main_keyboard: InlineKeyboardMarkup
    # если пользователь уже зареган, то заменяем
    # клавишу |Зарегистрироваться| на |Удалить аккаунт|
    if await UserCrud.is_user_registered(message.from_user.id):
        main_keyboard = get_main_keyboard("register")
    else:  # противоположная замена
        main_keyboard = get_main_keyboard()
    await message.answer(
        text=(
            f"<b>Рад Вас видеть, {message.from_user.full_name}!</b>\n\n{LEXICON['/start']}"
        ),
        reply_markup=main_keyboard,
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def command_help(message: Message):
    await message.answer(text=LEXICON["/help"])
