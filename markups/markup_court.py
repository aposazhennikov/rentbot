# ------------------- Profile Menu -------------------
"""В будущем здесь будеть кнопка найти оппонента, 
когда мы реализуем функцию рейтинга"""

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from titles import title
from models.user import User
from models.class_court import Calendar
from aiogram.types import KeyboardButton


async def main_menu(chat_id):
    title_court_1 = await title.load_title(chat_id, 'court_btn_court_1')
    title_court_2 = await title.load_title(chat_id, 'court_btn_court_2')
    title_location = await title.load_title(chat_id, 'court_btn_location')
    title_schedule = await title.load_title(chat_id, 'court_btn_schedule')
    title_main_menu = await title.load_title(chat_id, 'title_main_menu')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_court_1,
                              callback_data=f'court-show-1'),
            InlineKeyboardButton(text=title_court_2, callback_data=f'court-show-2')],
        [InlineKeyboardButton(text=title_location,
                              callback_data=f'court-show-location')],
        [InlineKeyboardButton(text=title_schedule,
                              callback_data=f'court-show-schedule')],
        [InlineKeyboardButton(text=title_main_menu,
                              callback_data=f'main-menu')],
    ])

    return keyboard


async def time_confirm(chat_id, id_court, date, time_start, time_end):
    title_yes = await title.load_title(chat_id, 'profile_btn_delete_yes')
    title_no = await title.load_title(chat_id, 'profile_btn_delete_no')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_yes,
                              callback_data=f'court-book-{id_court}-{date}-{time_start}-{time_end}'),
            InlineKeyboardButton(text=title_no, callback_data=f'court-get-timestart-{id_court}-{date}-{time_start}')],
        [InlineKeyboardButton(
            text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{id_court}-{date}')],
    ])

    return keyboard


async def days_menu(chat_id, id_court):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)
    structure = await court_manager.get_days()

    # lets make inline buttons for each
    for item in structure:
        callback = item[:10]
        btn = InlineKeyboardButton(
            text=item, callback_data=f'court-get-day-{id_court}-{callback}')
        keyboard_builder.add(btn)

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(3).as_markup()


async def location(chat_id, id_court):
    keyboard_builder = InlineKeyboardBuilder()

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()


async def schedule(chat_id, id_court):
    keyboard_builder = InlineKeyboardBuilder()

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()


async def time_start_menu(chat_id, id_court, date):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)
    structure = await court_manager.get_time()

    # lets make inline buttons for each
    for time in structure:
        btn = InlineKeyboardButton(
            text=time, callback_data=f'court-get-timestart-{id_court}-{date}-{time}')
        keyboard_builder.add(btn)

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-show-{id_court}')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(6).as_markup()


async def time_end_menu(chat_id, id_court, date, time_start):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)
    structure = await court_manager.get_time()
    q_slots_we_print = 1

    # lets make inline buttons for each
    for time in structure:
        split_ts = time_start.split(':')
        split_t = time.split(':')
        time_start_int = int(split_ts[0])
        time_int = int(split_t[0])

        if time_start == time:
            q_slots_we_print += 1
            title_btn = f'✅{time} ->'
            btn = InlineKeyboardButton(
                text=title_btn, callback_data=f'court-get-timeend-{id_court}-{date}-{time_start}-{time}')
            keyboard_builder.add(btn)

        if (time_start_int < time_int and court_manager.max_slots >= q_slots_we_print):
            q_slots_we_print += 1
            title_btn = time
            btn = InlineKeyboardButton(
                text=title_btn, callback_data=f'court-get-timeend-{id_court}-{date}-{time_start}-{time}')
            keyboard_builder.add(btn)

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{id_court}-{date}')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(3).as_markup()
