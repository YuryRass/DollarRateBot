from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from lexicon import LEXICON


router: Router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        text=LEXICON['/start']
    )


@router.message(Command(commands='help'))
async def command_help(message: Message):
    await message.answer(
        text=LEXICON['/help']
    )
