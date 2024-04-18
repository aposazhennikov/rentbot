from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()
    description = State()
