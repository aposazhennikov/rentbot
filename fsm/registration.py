from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    tennis_experience = State()
    ntrp = State()
    phone_number = State()
    description = State()
