from aiogram.fsm.state import State, StatesGroup


class DollarRateState(StatesGroup):
    start = State()
    history = State()
    registry = State()
    subscribe = State()
