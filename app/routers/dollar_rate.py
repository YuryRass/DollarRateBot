from datetime import datetime, timedelta

from faststream.rabbit.fastapi import RabbitRouter

from app.bot.v2.dollar_rate.schema import STelegramMessage
from app.config.config import settings
from app.scheduler.jobs import sending_dollar_rate
from app.scheduler.scheduler import scheduler

router = RabbitRouter(url=settings.RABBITMQ_URL)


@router.subscriber(settings.DOLLAR_RATE_QUEUE)
async def periodic_sending_dollar_rate(message_json: str) -> None:
    """Периодическая отправка курса доллара (раз в день) на протяжении 30 дней."""
    message = STelegramMessage.model_validate_json(json_data=message_json)
    current_datetime = datetime.now().replace(hour=23, minute=59, second=59)
    job_id = f"{settings.SHEDULER_SENDING_DOLLAR_RATE_PREFIX}_{message.chat_id}_{message.user_tg_id}"
    await sending_dollar_rate(message_json)
    scheduler.add_job(
        sending_dollar_rate,
        args=[message_json],
        trigger="interval",
        days=1,
        end_date=current_datetime + timedelta(days=30),
        id=job_id,
        replace_existing=True,
    )
