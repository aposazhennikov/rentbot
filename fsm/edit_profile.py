from aiogram.fsm.state import State, StatesGroup


class EditProfile(StatesGroup):
    first_name = State()
    last_name = State()
    ntrp = State()
    tennis_experience = State()
    birth_day = State()
    phone_number = State()
    description = State()
    gender = State()
