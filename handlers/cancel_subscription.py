from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command

from database.crud import add_subscription, is_user_subscribed
from keyboards import get_yes_no_keyboard


router: Router = Router()


@router.message(Command(commands='cancel_subscr'))
async def cancel_subscr_command(message: Message):
    if not await is_user_subscribed(message.from_user.id):
        await message.answer(
            text='У вас нет подписки, чтобы ее удалить!\n' +
            'Оформить подписку - /subscribe'
        )
        return
    yes_no_kb: InlineKeyboardMarkup = get_yes_no_keyboard()
    await message.answer(
        text='Вы уверены, что хотите отменить подписку???\n' +
        'Ведь деньги Вам не вернут 😒',
        reply_markup=yes_no_kb
    )


@router.callback_query(lambda answer: answer.data in ['yes', 'no'])
async def user_answer(callback: CallbackQuery):
    answer: str = callback.data
    callback.answer()
    if answer == 'no':
        await callback.message.answer(
            text='Ну и правильно! Подписка у Вас остается 😊'
        )
    else:
        await add_subscription(callback.from_user.id, False)
        await callback.message.answer(
            text='Подписка на каждодневное оповещение о курсе доллара удалена'
        )
