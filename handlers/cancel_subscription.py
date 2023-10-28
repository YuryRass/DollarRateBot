"""Отмена подписки"""

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from database import UserCrud
from keyboards import get_yes_no_keyboard


router: Router = Router()


class UserStates(StatesGroup):
    cancel_subscr = State()


@router.message(Command(commands='cancel_subscr'), StateFilter(default_state))
async def cancel_subscr_command(message: Message, state: FSMContext):
    if not await UserCrud.is_user_subscribed(message.from_user.id):
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
    await state.set_state(state=UserStates.cancel_subscr)


@router.callback_query(
    lambda answer: answer.data in ['yes', 'no'],
    StateFilter(UserStates.cancel_subscr)
)
async def user_answer(callback: CallbackQuery, state: FSMContext):
    answer: str = callback.data
    callback.answer()
    if answer == 'no':
        await callback.message.answer(
            text='Ну и правильно! Подписка у Вас остается 😊'
        )
    else:
        await UserCrud.add_subscription(callback.from_user.id, False)
        await callback.message.answer(
            text='Подписка на ежедневное оповещение о курсе доллара отменена'
        )
    await state.clear()
