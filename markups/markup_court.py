from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from titles import title
from models.class_court import Calendar
from models.booking import Booking
from datetime import datetime
from models.user import User


async def main_menu(chat_id):
    title_court = await title.load_title(chat_id, 'court_title')
    title_location = await title.load_title(chat_id, 'court_btn_location')
    # title_schedule = await title.load_title(chat_id, 'court_btn_schedule')
    title_my_booking = await title.load_title(chat_id, 'court_btn_booking_all')
    title_main_menu = await title.load_title(chat_id, 'title_main_menu')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{title_court} №1',
                              callback_data=f'court-get-1'),
            InlineKeyboardButton(text=f'{title_court} №2', callback_data=f'court-get-2')],
        [InlineKeyboardButton(text=title_location,
                              callback_data=f'court-get-location')],
        [InlineKeyboardButton(text=title_my_booking,
                              callback_data=f'court-get-book-{chat_id}')],
        [InlineKeyboardButton(text=title_main_menu,
                              callback_data=f'main-menu')],
    ])

    return keyboard


async def time_confirm(chat_id, court_id, date, time_start, time_end):
    title_yes = await title.load_title(chat_id, 'btn_yes')
    title_no = await title.load_title(chat_id, 'btn_no')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_yes,
                              callback_data=f'court-add-book-{court_id}-{date}-{time_start}-{time_end}'),
            InlineKeyboardButton(text=title_no, callback_data=f'court-get-timestart-{court_id}-{date}-{time_start}')],
        [InlineKeyboardButton(
            text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{court_id}-{date}')],
    ])

    return keyboard


async def days_menu(chat_id, court_id):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)

    # loading grade of user
    user_manager = User(chat_id)
    load_grade = await user_manager.get_user_args('grade')
    mdc = court_manager.max_days_calendar

    if mdc[int(load_grade['grade'])]:
        structure = await court_manager.get_days(mdc[int(load_grade['grade'])])
        max_day_in_line = court_manager.max_row_date
        # lets make inline buttons for each
        for item in structure:
            date = item[:10]
            btn = InlineKeyboardButton(
                text=item, callback_data=f'court-get-day-{court_id}-{date}')
            keyboard_builder.add(btn)

        btn_back = InlineKeyboardButton(
            text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
        keyboard_builder.add(btn_back)

        # buttom court menu
        btn_main_menu = InlineKeyboardButton(
            text=await title.load_title(chat_id, 'court_main'), callback_data=f'court-main')
        keyboard_builder.add(btn_main_menu)

        # court btn
        another_court = 2 if int(court_id) == 1 else 1

        title_court = await title.load_title(chat_id, 'court_title')
        btn_court = InlineKeyboardButton(text=f'{title_court} №{another_court}',
                                         callback_data=f'court-get-{another_court}')
        keyboard_builder.add(btn_court)

        # Calculate the number of columns based on the length of the structure
        if len(structure) <= max_day_in_line:
            columns = [max_day_in_line]
        else:
            columns = [max_day_in_line] * \
                (len(structure) // max_day_in_line)
            remaining_buttons = len(structure) % max_day_in_line
            if remaining_buttons:
                columns.append(remaining_buttons)

    return keyboard_builder.adjust(*columns, 3).as_markup()


async def location(chat_id, court_id):
    keyboard_builder = InlineKeyboardBuilder()

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()


async def schedule(chat_id, court_id):
    keyboard_builder = InlineKeyboardBuilder()

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='court-main')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()


async def time_start_menu(chat_id, court_id, date):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)
    structure = await court_manager.get_time_start()
    quantity_buttons = int()
    # get current time
    # today_day = datetime.now().strftime('%d.%m.%Y')
    # current_hour = datetime.now().strftime('%H')
    # current_minute = datetime.now().strftime('%M')
    current_timestamp = datetime.timestamp(datetime.now())

    # get booked time
    booking_manager = Booking(chat_id)
    booked_times = await booking_manager.get_times_by_datetime(date, court_id)

    # lets make inline buttons for each
    for slot_time in structure:
        slot_datetime = datetime.strptime(
            str(f'{date} {slot_time}'), '%d.%m.%Y %H:%M')
        slot_time_timestamp = datetime.timestamp(
            datetime.strptime(str(slot_datetime), '%Y-%m-%d %H:%M:%S'))

        # vars
        btn_title = ''
        btn_callback = ''

        if (slot_time_timestamp < current_timestamp):
            continue
        else:
            if booked_times:
                for booked_time in booked_times:
                    # b_time_start = datetime.strftime(booked_time[0], '%H:%M')
                    # b_time_end = datetime.strftime(booked_time[1], '%H:%M')
                    b_timestamp_start = datetime.timestamp(booked_time[0])
                    b_timestamp_end = datetime.timestamp(booked_time[1])
                    user_id = booked_time[2]

                    # timestamp algo
                    if (slot_time_timestamp >= b_timestamp_start and slot_time_timestamp < b_timestamp_end):
                        if (user_id == chat_id):
                            btn_title = f'✅{slot_time}'
                        else:
                            btn_title = f'❌{slot_time}'
                        btn_callback = f'court-get-book-{court_id}-{date}-{slot_time}'
                        continue

        #!!!! FUNCTION timestart and book we should combine bcz we can get error if someone cancel
        if btn_title == '' and btn_callback == '':
            btn_title = slot_time
            btn_callback = f'court-get-timestart-{court_id}-{date}-{slot_time}'

        quantity_buttons += 1

        btn = InlineKeyboardButton(
            text=btn_title, callback_data=btn_callback)
        keyboard_builder.add(btn)

    # all available dates
    structure = await court_manager.get_days_clear()
    current_date = datetime.strptime(str(date), "%d.%m.%Y")

    # rebuild structure to datetime format
    dates = [datetime.strptime(date, "%d.%m.%Y") for date in structure]
    # get index current date
    current_index = dates.index(current_date)
    # prev date if has
    previous_date = structure[current_index - 1] if current_index > 0 else None
    # next date if has
    next_date = structure[current_index +
                          1] if current_index < len(structure) - 1 else None

    # rebuilding to string
    previous_date_str = previous_date if previous_date else ""
    next_date_str = next_date if next_date else ""
    quantity_buttons_bottom = 0

    if (previous_date_str):
        btn_prev_date = InlineKeyboardButton(
            text=f'<< {previous_date_str}', callback_data=f'court-get-day-{court_id}-{previous_date_str}')
        keyboard_builder.add(btn_prev_date)
        quantity_buttons_bottom += 1

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-{court_id}')
    keyboard_builder.add(btn_back)
    quantity_buttons_bottom += 1

    if (next_date_str):
        btn_next_date = InlineKeyboardButton(
            text=f'{next_date_str} >>', callback_data=f'court-get-day-{court_id}-{next_date_str}')
        keyboard_builder.add(btn_next_date)
        quantity_buttons_bottom += 1

    # Calculate the number of columns based on the length of the structure
    if quantity_buttons <= court_manager.max_row_time:
        columns = [quantity_buttons]
    else:
        columns = [court_manager.max_row_time] * \
            (quantity_buttons // court_manager.max_row_time)
        remaining_buttons = quantity_buttons % court_manager.max_row_time

        if remaining_buttons:
            columns.append(remaining_buttons)

    # btn another court
    another_court = 1 if int(court_id) == 2 else 2
    title_another_court = await title.load_title(chat_id, 'court_another_title', another_court, date)

    btn_another_court = InlineKeyboardButton(
        text=title_another_court, callback_data=f'court-get-day-{another_court}-{date}')
    keyboard_builder.add(btn_another_court)

    return keyboard_builder.adjust(*columns, quantity_buttons_bottom, 1).as_markup()


async def get_booking(chat_id, court_id, date):
    keyboard_builder = InlineKeyboardBuilder()

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{court_id}-{date}')
    keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()


async def get_booking_self(chat_id, court_id, date, book_id):
    keyboard_builder = InlineKeyboardBuilder()

    title_delete = await title.load_title(chat_id, 'btn_delete')
    title_all = await title.load_title(chat_id, 'court_btn_booking_all')
    btn_get_all = InlineKeyboardButton(
        text=title_all, callback_data=f'court-get-book-{chat_id}')
    btn_delete = InlineKeyboardButton(
        text=title_delete, callback_data=f'court-delete-book-{book_id}')
    btn_back = InlineKeyboardButton(
        text=f'< {date} >', callback_data=f'court-get-day-{court_id}-{date}')
    keyboard_builder.add(btn_get_all, btn_delete, btn_back)

    return keyboard_builder.adjust(2, 1).as_markup()


async def time_end_menu(chat_id, court_id, date, time_start, count_slots):
    keyboard_builder = InlineKeyboardBuilder()
    court_manager = Calendar(chat_id)
    structure = await court_manager.get_time_end()
    q_slots_we_print = count_slots
    quantity_buttons = 0
    booking_manager = Booking(chat_id)

    if (q_slots_we_print < court_manager.max_slots):
        booked_times = await booking_manager.get_times_by_datetime(date, court_id, time_start)

        # lets make inline buttons for each
        for slot_time in structure:
            slot_datetime = datetime.strptime(
                str(f'{date} {slot_time}'), '%d.%m.%Y %H:%M')
            slot_time_timestamp = datetime.timestamp(
                datetime.strptime(str(slot_datetime), '%Y-%m-%d %H:%M:%S'))

            if booked_times:
                for booked_time in booked_times:
                    b_timestamp_start = datetime.timestamp(booked_time[0])
                    b_timestamp_end = datetime.timestamp(booked_time[1])

                    if (slot_time_timestamp > b_timestamp_start and slot_time_timestamp <= b_timestamp_end):
                        # print(f'booked: {slot_time} {slot_time_timestamp}')
                        q_slots_we_print = court_manager.max_slots + 1
                        continue

            if (q_slots_we_print > court_manager.max_slots):
                continue

            split_ts = time_start.split(':')
            slot_time_split = slot_time.split(':')
            start_hour_int = int(split_ts[0])
            start_minute_int = int(split_ts[1])
            slot_hour_int = int(slot_time_split[0])
            slot_minute_int = int(slot_time_split[0])

            title_btn = ''

            if time_start == slot_time:
                title_btn = f'✅{slot_time} >>'
            else:
                # 12 == 12
                if (start_hour_int == slot_hour_int):
                    # 00>30
                    if (start_minute_int > slot_minute_int):
                        # print(f'skip {slot_time}')
                        continue
                    else:
                        title_btn = slot_time

                elif (start_hour_int < slot_hour_int):
                    title_btn = slot_time
                else:
                    continue

            q_slots_we_print += 1
            btn = InlineKeyboardButton(
                text=title_btn, callback_data=f'court-get-timeend-{court_id}-{date}-{time_start}-{slot_time}')
            keyboard_builder.add(btn)
            quantity_buttons += 1

    else:
        print('no slots')

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{court_id}-{date}')
    keyboard_builder.add(btn_back)

    if (quantity_buttons):
        # Calculate the number of columns based on the length of the structure
        if quantity_buttons <= court_manager.max_row_time:
            columns = [quantity_buttons]
        else:
            columns = [court_manager.max_row_time] * \
                (quantity_buttons // court_manager.max_row_time)
            remaining_buttons = quantity_buttons % court_manager.max_row_time

            if remaining_buttons:
                columns.append(remaining_buttons)
        return keyboard_builder.adjust(*columns, 1).as_markup()
    else:
        return keyboard_builder.adjust(1).as_markup()

    # return keyboard_builder.adjust(3).as_markup()


async def delete_status(chat_id, court_id, date):
    keyboard_builder = InlineKeyboardBuilder()
    title_all = await title.load_title(chat_id, 'court_btn_booking_all')
    btn_get_all = InlineKeyboardButton(
        text=title_all, callback_data=f'court-get-book-{chat_id}')

    btn_back = InlineKeyboardButton(
        text=f'< {date}', callback_data=f'court-get-day-{court_id}-{date}')
    keyboard_builder.add(btn_get_all, btn_back)
    return keyboard_builder.adjust(1).as_markup()


async def back_date(chat_id, court_id, date):
    keyboard_builder = InlineKeyboardBuilder()
    title_all = await title.load_title(chat_id, 'court_btn_booking_all')
    btn_get_all = InlineKeyboardButton(
        text=title_all, callback_data=f'court-get-book-{chat_id}')

    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data=f'court-get-day-{court_id}-{date}')
    keyboard_builder.add(btn_get_all, btn_back)

    return keyboard_builder.adjust(1).as_markup()


# court_book_list
async def booking_list(chat_id, bookings, data_fsm):
    keyboard_builder = InlineKeyboardBuilder()

    if bookings:
        for book in bookings:
            court_id = int(book['court_id'])
            date = str(book['date'].strftime('%d.%m.%Y'))
            slot_time = str(book['start_time'].strftime('%H:%M'))
            court_sticker = "1️⃣" if int(book['court_id']) == 1 else "2️⃣"
            title_btn = f"{court_sticker} {book['date'].strftime('%d.%m.%Y')} {book['start_time'].strftime('%H:%M')}-{book['end_time'].strftime('%H:%M')}\n"
            btn_callback = f'court-get-book-{court_id}-{date}-{slot_time}'
            btn = InlineKeyboardButton(
                text=title_btn, callback_data=btn_callback)
            keyboard_builder.add(btn)

    # buttom main menu
    title_main_menu = await title.load_title(chat_id, 'court_main')
    btn_court_main = InlineKeyboardButton(
        text=title_main_menu, callback_data=f'court-main')
    title_main_menu = await title.load_title(chat_id, 'title_main_menu')
    btn_main_menu = InlineKeyboardButton(
        text=title_main_menu, callback_data=f'main-menu')
    keyboard_builder.add(btn_court_main, btn_main_menu)

    if (len(data_fsm) > 0 and data_fsm.get('url_from')):
        btn_back = InlineKeyboardButton(
            text=await title.load_title(chat_id, 'btn_back'), callback_data=data_fsm.get('url_from'))
        keyboard_builder.add(btn_back)

    return keyboard_builder.adjust(1).as_markup()
