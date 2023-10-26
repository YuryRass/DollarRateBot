from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsUserCommand(BaseFilter):
    command: str | None = None

    def __init__(self, command: str):
        self.command = command

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.command
