from datetime import datetime

from app.bot.v2.create_bot import BOT
from app.bot.v2.dollar_rate.schema import STelegramMessage
from app.services.dollar_rate import DollarRateService


async def sending_dollar_rate(message_json: str) -> None:
    message = STelegramMessage.model_validate_json(json_data=message_json)
    dollar_rate = await DollarRateService.get_and_save_dollar_rate(message.user_tg_id)
    sending_msg = f"{datetime.now().strftime('%d/%m/%Y %H:%M')} -> курс доллара: {dollar_rate} руб."
    await BOT.send_message(message.chat_id, sending_msg)
