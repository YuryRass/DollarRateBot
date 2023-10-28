from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database.crud import delete_account
from keyboards import get_yes_no_keyboard
from filters import IsUserCommand


router: Router = Router()


async def _delete_account(info: Message | CallbackQuery):
    if isinstance(info, CallbackQuery):
        info = info.message
    await info.answer(
        text='Вы уверены, что хотите удалить свой аккаунт?',
        reply_markup=get_yes_no_keyboard('delete'),
    )


@router.message(Command(commands='unregistry'))
async def delete_account_command(message: Message):
    await _delete_account(message)


@router.callback_query(IsUserCommand('unregistry'))
async def del_account(callback: CallbackQuery):
    await callback.answer()
    await _delete_account(callback)


@router.callback_query(lambda answer: 'delete' in answer.data)
async def delete_user_account(callback: CallbackQuery):
    if callback.data.endswith('no'):
        await callback.message.answer(
            text='Ну и правильно!'
        )
    # yes
    else:
        await delete_account(callback.from_user.id)
        await callback.message.answer(
            text='Ваш аккаунт удалён!'
        )
