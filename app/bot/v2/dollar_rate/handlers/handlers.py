from aiogram import F, Router
from aiogram.filters.command import CommandStart
from aiogram.types import (
    CallbackQuery,
    ContentType,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from app.bot.v2.create_bot import BOT
from app.bot.v2.dollar_rate.state import DollarRateState
from app.config.config import settings
from app.services.dollar_rate import DollarRateService
from app.services.user import UserService

router = Router()

PRICE = LabeledPrice(label="Подписка на 1 месяц", amount=100 * 100)  # 100 руб.
DAY = 24 * 60 * 60


@router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager) -> None:
    await UserService.add_user(user_tg_id=message.from_user.id)
    await dialog_manager.start(state=DollarRateState.start, mode=StartMode.RESET_STACK)


async def dollar_price(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    dollar_price = await DollarRateService.get_and_save_dollar_rate(
        callback.from_user.id
    )
    await callback.message.answer(f"Курс доллара: {dollar_price} руб.")


async def dollar_history(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=DollarRateState.history, mode=StartMode.NEW_STACK)


async def user_registry(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if not await UserService.is_user_registered(callback.from_user.id):
        await manager.switch_to(state=DollarRateState.registry, show_mode=ShowMode.SEND)
    else:
        await callback.message.answer(text="Вы уже зарегистрированы!")


async def correct_fullname_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    await UserService.add_user_fullname(message.from_user.id, text)
    await message.answer(
        text=(
            "Поздравляю! Теперь Вы зарегестрированы и "
            "можете оформить подписку, чтобы получать оповещения о курсе "
            "доллара каждый день"
        )
    )
    await dialog_manager.start(state=DollarRateState.start)


async def error_fullname_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
) -> None:
    await message.answer(
        text="ФИО введены некорректно! Попробуйте еще раз",
    )
    await dialog_manager.start(state=DollarRateState.start)


async def user_subscription(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if await UserService.is_user_subscribed(callback.from_user.id):
        await callback.message.answer(text="У вас уже есть подписка!")
        return
    if not await UserService.is_user_registered(callback.from_user.id):
        await callback.message.answer(text=("Вы не зарегистрированы!\n"))
        return
    if settings.PAYMENTS_TOKEN.split(":")[1] == "TEST":
        await callback.message.answer(text="Это тестовый платеж 🤑")

    await callback.message.answer_invoice(
        title="Подписка на оповещения",
        description="Активация подписки на 1 месяц",
        provider_token=settings.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload",
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery) -> None:
    await pre_checkout_q.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await message.answer(
        text=(
            "Платеж на сумму "
            f"{message.successful_payment.total_amount // 100} "
            f"{message.successful_payment.currency} прошел успешно!\n\n"
            "Теперь Вам будут приходить оповещения о курсе доллара каждый день\n"
        )
    )
    await UserService.add_subscription(message.from_user.id)
    await BOT.send_message(
        chat_id=message.chat.id, text="Здесь скоро будет периодическая отправка!!!"
    )


# TODO периодическая задача
# async def regular_dollar_rate(message: Message) -> None:
#     while True:
#         if not await UserService.is_user_subscribed(message.from_user.id):
#             break
#         dollar_price = await DollarRateService.get_and_save_dollar_rate(
#             message.from_user.id
#         )
#         await message.answer(
#             text=(
#                 f"Курс доллара: {dollar_price} руб.\n"
#                 "Следующее оповещение будет через 24 часа "
#                 f"в {datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M')} по мск."
#             )
#         )

#         # засыпаем на сутки
#         await asyncio.sleep(DAY)


BUTTON_MAPPER = {
    "dollar": dollar_price,
    "subscribe": user_subscription,
    "history": dollar_history,
    "register": user_registry,
}
