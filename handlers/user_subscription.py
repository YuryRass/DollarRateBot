"""
    Подписка пользователя на каждодневное получении информации о курсе доллара
"""
import asyncio
from datetime import datetime
from aiogram import Router, F
from aiogram.types import \
    CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.state import default_state
from aiogram.filters import Command, StateFilter

from filters import IsUserCommand, IsUserSubscribed
from database import UserCrud
from api_requests import DollarConverter
from config import settings

DAY = 24 * 60 * 60
router: Router = Router()


PRICE = LabeledPrice(
    label="Подписка на 1 месяц",
    amount=100*100
)  # в копейках (руб)


async def _user_subscription(info: Message | CallbackQuery):
    user_tg_id: int = info.from_user.id
    if isinstance(info, CallbackQuery):
        info = info.message
    if await UserCrud.is_user_subscribed(user_tg_id):
        await info.answer(
            text='У вас уже есть подписка!'
        )
        return
    if not await UserCrud.is_user_registered(user_tg_id):
        await info.answer(
            text='Вы не зарегистрированы!\n' +
            'Для регистрации используйте /register'
        )
        return
    if settings.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await info.answer(text="Это тестовый платеж 🤑")

    await info.answer_invoice(
        title="Подписка на оповещения",
        description="Активация подписки на 1 месяц",
        provider_token=settings.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )


@router.message(Command(commands='subscribe'), StateFilter(default_state))
async def user_subscription_command(message: Message):
    await _user_subscription(message)


@router.callback_query(IsUserCommand('subscribe'), StateFilter(default_state))
async def user_subscription(callback: CallbackQuery):
    await _user_subscription(callback)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer(
        text='Платеж на сумму ' +
        f'{message.successful_payment.total_amount // 100} ' +
        f'{message.successful_payment.currency} прошел успешно!\n\n' +
        'Теперь Вам будут приходить оповещения о курсе доллара каждый день\n' +
        '/begin - начать оповещения'
    )
    await UserCrud.add_subscription(message.from_user.id)


@router.message(IsUserSubscribed())
async def regular_dollar_rate(message: Message):
    while True:
        if not await UserCrud.is_user_subscribed(message.from_user.id):
            break
        dollar_price: float = await DollarConverter.get_price()
        await message.answer(
            text=f'Курс доллара: {dollar_price} руб.\n' +
            'Следующее оповещение будет через 24 часа ' +
            f'в {datetime.now().strftime("%H:%M")}'
        )
        await UserCrud.save_dollar_price(message.from_user.id, dollar_price)

        # засыпаем на сутки
        await asyncio.sleep(DAY)


@router.message(Command(commands='begin'))
async def user_is_not_subscribed(message: Message):
    await message.answer(
        'У Вас нет подписки 😢\n/subscribe - оформить подписку'
    )
