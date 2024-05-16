from models.user import User
from models.booking import Booking
from markups import markup_profile
from aiogram.filters import Command
from aiogram.types import Message
from titles import title
from config import *
from aiogram import Router
from models.class_court import Calendar
router_profile = Router()


@router_profile.message(Command('profile'))
async def command_profile_handler(message: Message) -> None:
    user_manager = User(message.chat.id)
    user_load = await user_manager.get()

    if (user_load):
        booking_manager = Booking(message.chat.id)
        message_out = await get_profile_info(message.chat.id, user_load)

        # showing how much slots user booked
        if (1 == 2):
            count_slots = await booking_manager.calculate_intervals_count()

            if count_slots:
                message_out += f'\n count slots: {count_slots}'
            else:
                print(f'no count:{count_slots}')
        await message.answer(message_out, reply_markup=await markup_profile.main_menu(message.chat.id))
    else:
        # run registration
        await message.answer('u should reg')


async def get_profile_info(chat_id, user_load):
    # we have to check and print each field if it exists in order. but now from TT

    out = await title.load_title(chat_id, 'profile_main_menu')
    user_manager = User(chat_id)
    fields = await user_manager.get_fields_show_profile()
    grade_list = await user_manager.get_grade_list()
    print(grade_list)

    for field in fields:
        if (user_load[field] != None):
            if field == 'gender':
                if user_load[field] == 'male':
                    field_value = "🚹"
                elif user_load[field] == 'female':
                    field_value = "🚺"
                else:
                    field_value = user_load[field]
            elif field == 'grade':
                field_value = grade_list[user_load[field]]
            else:
                field_value = user_load[field]
            title_field = await title.load_title(chat_id, f'title_field_{field}')
            capitalized_word = title_field[0].upper() + title_field[1:]
            out += f'<b>{capitalized_word}</b> : {field_value}\n'

    # if user_load['is_admin']:
    grade = int(user_load['grade'])
    out += f'\n\n=== week stats ===\n'
    # out += f'🫥 user is Admin\n'

    calendar_manager = Calendar(chat_id)
    booking_manager = Booking(chat_id)
    intervals = await booking_manager.calculate_intervals_count()
    print(intervals)

    already_booking = intervals['booking'] if intervals else 0
    already_booked_all = intervals['slots_all'] if intervals else 0
    already_booked_weekday = intervals['slots_weekday'] if intervals else 0
    slots_primetime = intervals['slots_primetime'] if intervals else 0
    out += f'days in calendar: {calendar_manager.max_days_calendar[grade]}\n'
    out += f'booking per week: {already_booking}/{calendar_manager.max_booking_week[grade]}\n'
    out += f'slots weekday: {already_booked_weekday}/{calendar_manager.max_slots_per_day}\n'
    out += f'slots primetime: {slots_primetime}/{calendar_manager.max_slots_primetime}\n'
    out += f'total slots: {already_booked_all}\n'
    # out += f'max slots weekends: {already_booked_weekends}/{calendar_manager.max_slots_primetime}\n'
    # out += f'intervals: {intervals}\n'

    return out
