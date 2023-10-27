from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsUserCommand(BaseFilter):
    command: str | None = None

    def __init__(self, command: str):
        self.command = command

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.command


class IsPaginatorBtn(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, int]:
        paginator: int
        if 'paginator' in callback.data:
            paginator = int(callback.data.split('_')[1])
            return {'paginator': paginator}


class IsNotCallBack(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'not_call'
