"""Обработка команд /start и /help"""

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import InlineKeyboardMarkup, Message

from bot.v1.keyboards import get_main_keyboard
from bot.v1.lexicon import LEXICON
from services.user import UserService

router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start(message: Message):
    # добавление пользователя, если его нет в таблице
    await UserService.add_user(user_tg_id=message.from_user.id)

    # главная клавиатура для пользователя
    main_keyboard: InlineKeyboardMarkup
    # если пользователь уже зареган, то заменяем
    # клавишу |Зарегистрироваться| на |Удалить аккаунт|
    if await UserService.is_user_registered(user_tg_id=message.from_user.id):
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
