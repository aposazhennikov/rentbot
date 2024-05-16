from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile
from aiogram import Router
from aiogram.fsm.context import FSMContext
from fsm.menu import Menu
from markups import markup_court
from titles import title
from models.booking import Booking
from models.class_court import Calendar
from datetime import datetime
import re

router_court_callback = Router()


@router_court_callback.callback_query()
async def handle_profile_callback(callback: CallbackQuery, state=FSMContext):

    # get back call-back
    data_fsm = await state.get_data()

    print(f'fsm: {data_fsm}')

    if (data_fsm.get('url_from') != callback.data or len(data_fsm) == 0):
        await state.set_state(Menu.url_from)
        await state.update_data(url_from=callback.data)

    print(f'fsm: {data_fsm}')

    split = callback.data.split('-')
    print(split)
    chat_id = callback.message.chat.id
    # print('======\n')
    # print(callback)
    # prefix - COURT
    if len(split) == 2:
        prefix, action = split

        if action == 'main':
            await callback.message.edit_text(await title.load_title(callback.message.chat.id, 'court_main'), reply_markup=await markup_court.main_menu(callback.message.chat.id))

        await callback.answer(action)

    elif len(split) == 3:
        prefix, action, field = split

        if (action == 'get'):
            if field == 'location':
                # photo_id = 'AgACAgIAAxkBAAIHRGY6Qf53Kl9n925Ncl7SxyvOG7VuAAL92zEbrmDQSXmF12wN295cAQADAgADeAADNQQ'
                # await callback.message.bot.send_photo(chat_id, photo_id)
                out = await title.load_title(chat_id, 'court_location') + '\n'
                out += await title.load_title(chat_id, 'court_title') + ' 1 ' + await title.load_title(chat_id, 'system_link_court_first') + '\n'
                out += await title.load_title(chat_id, 'court_title') + ' 2 ' + await title.load_title(chat_id, 'system_link_court_second') + '\n'
                await callback.message.edit_text(out, reply_markup=await markup_court.location(chat_id, field))
            elif field == 'schedule':
                await callback.message.edit_text(await title.load_title(chat_id, 'court_schedule'), reply_markup=await markup_court.schedule(chat_id, field))
            else:
                if int(field) in [1, 2]:
                    court = field
                    await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_day', court), reply_markup=await markup_court.days_menu(chat_id, field))
                else:
                    # i dont know how u got it, error
                    pass
        else:
            # i dont know how u got it, error
            pass
    elif len(split) == 4:
        prefix, action, entity, field = split

        if (action == 'get'):
            if entity == 'book':
                # print('book list')
                booking_manager = Booking(chat_id)
                bookings = await booking_manager.get_all()

                if bookings:
                    await callback.message.edit_text(await title.load_title(chat_id, 'court_book_list'), reply_markup=await markup_court.booking_list(field, bookings, data_fsm))
                else:
                    await callback.message.edit_text(await title.load_title(chat_id, 'court_book_list_empty'), reply_markup=await markup_court.booking_list(field, bookings, data_fsm))

                # await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_time_start', field), reply_markup=await markup_court.time_start_menu(chat_id, field))
            else:
                # i dont know how u got it, error
                pass
        elif (action == 'delete'):
            if entity == 'book':
                booking_manager = Booking(chat_id)
                data_booking = await booking_manager.get(field)

                if (data_booking):
                    date = str(data_booking['date'].strftime("%d.%m.%Y"))
                    court = int(data_booking['court_id'])
                    is_delete = await booking_manager.delete(field)
                    status_delete = await title.load_title(chat_id, 'court_delete_success') if is_delete else await title.load_title(chat_id, 'court_delete_fail')
                    await callback.message.edit_text(status_delete, reply_markup=await markup_court.delete_status(chat_id, court, date))
            else:
                # i dont know how u got it, error
                pass
        else:
            # i dont know how u got it, error
            pass

    elif len(split) == 5:
        prefix, action, entity, court, date = split

        if (int(court) in [1, 2]):
            if (action == 'get'):
                if entity == 'day':
                    # here is we load time for day=date
                    await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_time_start', court, date), reply_markup=await markup_court.time_start_menu(chat_id, court, date))
                else:
                    # i dont know how u got it, error
                    pass
            else:
                # i dont know how u got it, error
                pass
        else:
            # i dont know how u got it, error
            pass

    elif len(split) == 6:
        prefix, action, entity, court, date, time = split

        if action == 'get':
            if entity == 'timestart':
                if (int(court) in [1, 2]):
                    # here is we load time for day=date
                    booking_manager = Booking(chat_id)
                    court_manager = Calendar(chat_id)
                    # check already taken
                    intevals = await booking_manager.calculate_intervals_count()
                    if intevals:
                        count_slots = intevals['slots_all']
                    else:
                        count_slots = 0
                    if (count_slots < court_manager.max_slots):
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_time_end', court, date, time), reply_markup=await markup_court.time_end_menu(chat_id, court, date, time, count_slots))
                    else:
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_error_no_slots', count_slots, court_manager.max_slots), reply_markup=await markup_court.back_date(chat_id, court, date))

                else:
                    # i dont know how u got it, error
                    pass
            elif entity == 'book':
                if (int(court) in [1, 2]):
                    booking_manager = Booking(chat_id)
                    data_booking = await booking_manager.get_user_by_datetime(date, court, time)

                    if (data_booking):
                        user_name = data_booking['first_name']

                        if (data_booking['user_name']):
                            user_name += ' ' + data_booking['user_name']
                        b_time_start = datetime.strftime(
                            data_booking['start_time'], '%H:%M')
                        b_time_end = datetime.strftime(
                            data_booking['end_time'], '%H:%M')

                        if (data_booking['user_id'] == chat_id):
                            # print('watch self book')
                            await callback.message.edit_text(await title.load_title(chat_id, 'court_get_booking_self', court, date, b_time_start, b_time_end, user_name), reply_markup=await markup_court.get_booking_self(chat_id, court, date, data_booking['id']))
                        else:
                            print(data_booking)
                            await callback.message.edit_text(await title.load_title(chat_id, 'court_get_booking', court, date, b_time_start, b_time_end, user_name), reply_markup=await markup_court.get_booking(chat_id, court, date))
                    else:
                        print('error get booking')
                        pass
            else:
                # i dont know how u got it, error
                pass
    elif len(split) == 7:
        prefix, action, entity, court, date, time_start, time_end = split

        if (int(court) in [1, 2]):
            # if callback is get-1 or get-2 that means court 1 or court 2
            if entity == 'timeend':
                if time_start == time_end:
                    # here is we load time for day=date
                    booking_manager = Booking(chat_id)
                    court_manager = Calendar(chat_id)
                    # check already taken
                    intevals = await booking_manager.calculate_intervals_count()
                    if intevals:
                        count_slots = intevals['slots_all']
                    else:
                        count_slots = 0

                    if (count_slots < court_manager.max_slots):
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_time_end_same', court, date, time_start), reply_markup=await markup_court.time_end_menu(chat_id, court, date, time_start, count_slots))
                    else:
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_error_no_slots', count_slots, court_manager.max_slots), reply_markup=await markup_court.back_date(chat_id, court, date))
                else:
                    # here is we load time for day=date
                    title_court = await title.load_title(chat_id, 'court_title')
                    message_out = f'{title_court} №{court}\n'
                    message_out += f'{date}\n'
                    message_out += f'{time_start} - {time_end}'
                    message_out += '\n\n'
                    message_out += await title.load_title(chat_id, 'court_book_confirm')

                    await callback.message.edit_text(message_out, reply_markup=await markup_court.time_confirm(chat_id, court, date, time_start, time_end))
            elif action == 'add' and entity == 'book':
                if (int(court) in [1, 2]):
                    # here is we load time for day=date
                    booking_manager = Booking(chat_id)

                    time_start_formatted = datetime.strptime(
                        f'{date} {time_start}', '%d.%m.%Y %H:%M').strftime('%Y-%m-%dT%H:%M:%S.%f')
                    time_end_formatted = datetime.strptime(
                        f'{date} {time_end}', '%d.%m.%Y %H:%M').strftime('%Y-%m-%dT%H:%M:%S.%f')
                    date_formatted = datetime.strptime(
                        date, '%d.%m.%Y').strftime('%Y-%m-%d')

                    is_booked = await booking_manager.create(
                        {'court_id': court, 'date': date_formatted, 'start_time': time_start_formatted, 'end_time': time_end_formatted, 'user_id': chat_id})

                    if is_booked:
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_booked'), reply_markup=await markup_court.time_start_menu(chat_id, court, date))
                    else:
                        await callback.message.edit_text(await title.load_title(chat_id, 'court_book_error'), reply_markup=await markup_court.time_start_menu(chat_id, court, date))
            else:
                # i dont know how u got it, error
                pass
        else:
            # i dont know how u got it, error
            pass

    else:
        print(f'count: {len(split)}')
