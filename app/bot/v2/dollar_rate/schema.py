from pydantic import BaseModel


class STelegramMessage(BaseModel):
    chat_id: int
    user_tg_id: int
