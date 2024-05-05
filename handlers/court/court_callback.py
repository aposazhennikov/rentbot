from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram.fsm.context import FSMContext
from markups import markup_court
import re
from titles import title

router_court_callback = Router()


@router_court_callback.callback_query(lambda c: re.match(r'court-', c.data))
async def handle_profile_callback(callback: CallbackQuery, state=FSMContext):
    split = callback.data.split('-')
    print(split)
    chat_id = callback.message.chat.id

    if len(split) == 2:
        prefix, action = split

        if action == 'main':
            await callback.message.edit_text(await title.load_title(callback.message.chat.id, 'court_main'), reply_markup=await markup_court.main_menu(callback.message.chat.id))

        await callback.answer(action)

    elif len(split) == 3:
        prefix, action, field = split

        # if callback is show-1 or show-2 that means court 1 or court 2
        if (action == 'show'):
            if field == 'location':
                await callback.message.edit_text(await title.load_title(chat_id, 'court_location'), reply_markup=await markup_court.location(chat_id, field))
            elif field == 'schedule':
                await callback.message.edit_text(await title.load_title(chat_id, 'court_schedule'), reply_markup=await markup_court.schedule(chat_id, field))
            else:
                if int(field) in [1, 2]:
                    await callback.message.edit_text(await title.load_title(chat_id, 'court_choice_day'), reply_markup=await markup_court.days_menu(chat_id, field))
                else:
                    # i dont know how u got it, error
                    pass
        else:
            # i dont know how u got it, error
            pass
    # here is we got calendar
    elif len(split) == 5:
        prefix, action, entity, court, date = split

        if (int(court) in [1, 2]):
            # if callback is show-1 or show-2 that means court 1 or court 2
            if (action == 'get'):
                if entity == 'day':
                    # here is we load time for day=date
                    await callback.message.edit_text("Выберите начало", reply_markup=await markup_court.time_start_menu(chat_id, court, date))
                else:
                    # i dont know how u got it, error
                    pass
            else:
                # i dont know how u got it, error
                pass
        else:
            # i dont know how u got it, error
            pass
    # here is we got calendar
    elif len(split) == 6:
        prefix, action, entity, court, date, time = split

        # if callback is show-1 or show-2 that means court 1 or court 2
        if entity == 'timestart':
            if (int(court) in [1, 2]):
                # here is we load time for day=date
                await callback.message.edit_text("Выберите окончание", reply_markup=await markup_court.time_end_menu(chat_id, court, date, time))
            else:
                # i dont know how u got it, error
                pass
        elif action == 'book':
            pass
        else:
            # i dont know how u got it, error
            pass
    # here is we got calendar
    elif len(split) == 7:
        prefix, action, entity, court, date, time_start, time_end = split

        if (int(court) in [1, 2]):
            # if callback is show-1 or show-2 that means court 1 or court 2
            if entity == 'timeend':
                # here is we load time for day=date
                message_out = f'Корт №{court}\n'
                message_out += f'{date}\n'
                message_out += f'{time_start} - {time_end}'
                await callback.message.edit_text(message_out, reply_markup=await markup_court.time_confirm(chat_id, court, date, time_start, time_end))
            else:
                # i dont know how u got it, error
                pass
        else:
            # i dont know how u got it, error
            pass
    else:
        print(f'count: {len(split)}')
