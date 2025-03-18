from typing import Any

from aiogram.types import User

from app.database.models import DollarHistory
from app.services.user import UserService


async def get_user_full_name(event_from_user: User, **kwargs: Any) -> dict:
    return {"user_full_name": event_from_user.full_name}


async def get_dollar_history(event_from_user: User, **kwargs: Any) -> dict:
    dollar_history: list[DollarHistory] = await UserService.get_user_history(
        event_from_user.id
    )

    return {
        "history": [
            (
                (
                    f"{history.date_time.strftime('%d.%m.%y %H:%M:%S')} "
                    f"💵 {history.cost_value} руб."
                ),
                history.id,
            )
            for history in dollar_history
        ],
        "len_history": len(dollar_history),
    }
