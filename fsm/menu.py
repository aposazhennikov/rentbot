from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    url_from = State()
