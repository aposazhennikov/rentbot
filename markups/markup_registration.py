from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Titles contains function load_json/load_title/save_user_language/get_user_language this is needed for
# work with translations and response to users
from titles import title


async def inline_ntrp_quest(chat_id):
    ''' NEED TO ADD FUNCTION DESCRIPTION '''
    
    title_btn_yes = title.load_title(chat_id, 'reg_ntrp_btn_yes')
    title_btn_no = title.load_title(chat_id, 'reg_ntrp_btn_no')
    # way 1
        # keyboard_builder = InlineKeyboardBuilder()
        # btn_yes = InlineKeyboardButton(text=title_btn_yes, callback_data='reg_ntrpyes')
        # btn_no = InlineKeyboardButton(text=title_btn_no, callback_data='reg_ntrpno')
        # keyboard_builder.add(btn_yes)
        # keyboard_builder.add(btn_no)
        # keyboard_builder.adjust(2).as_markup()
        # return keyboard_builder.adjust(2).as_markup()
        # Билдеры пригодятся для расписания например, когда у нас разное кол-во кнопок в меню будет...
    # way 2
    # Тут списками регулируется положение кнопок, сколько в одном ряду будет кнопок [btn1, btn2] - две кнопки в одном ряду.
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=title_btn_yes, callback_data='reg_ntrpyes'),
                        InlineKeyboardButton(text=title_btn_no, callback_data='reg_ntrpno')]])
    return keyboard
   


async def inline_ntrp_accept(chat_id):
    ''' NEED TO ADD DESCRIPTION '''
    # way 2
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=title.load_title(chat_id, 'reg_ntrp_btn_accept'),
                              callback_data='reg_ntrpyes')]])
    return keyboard
    # return keyboard_builder.adjust(2).as_markup()
