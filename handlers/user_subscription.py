from aiogram import Router, F
from aiogram.types import \
    CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from filters import IsUserCommand
from database.crud import is_user_registered
from config import settings


router: Router = Router()

PRICE = LabeledPrice(
    label="Подписка на 1 месяц",
    amount=500*100
)  # в копейках (руб)


@router.message(Command(commands='subscribe'), StateFilter(default_state))
async def user_subscription_command(message: Message):
    if not await is_user_registered(message.from_user.id):
        await message.answer(
            text='Вы не зарегистрированы!\n' +
            'Для регистрации используйте /registry'
        )
        return

    if settings.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await message.answer(text="Это тестовый платеж 🤑")

    await message.answer_invoice(
        title="Подписка на оповещения",
        description="Активация подписки на 1 месяц",
        provider_token=settings.PAYMENTS_TOKEN,
        currency="rub",
        # photo_url="",
        # photo_width=416,
        # photo_height=234,
        # photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

# pre checkout  (must be answered in 10 seconds)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


# successful payment
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await message.answer(
        text='Платеж на сумму ' +
        f'{message.successful_payment.total_amount // 100} ' +
        f'{message.successful_payment.currency} прошел успешно!!!'
    )
