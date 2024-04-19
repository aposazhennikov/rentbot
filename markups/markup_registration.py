from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from titles import title


async def inline_ntrp_quest(chat_id):
    # way 1
    title_btn_yes = title.load_title(chat_id, 'reg_ntrp_btn_yes')
    title_btn_no = title.load_title(chat_id, 'reg_ntrp_btn_no')
    keyboard_builder = InlineKeyboardBuilder()

    btn_yes = InlineKeyboardButton(
        text=title_btn_yes, callback_data='reg_ntrpyes')
    btn_no = InlineKeyboardButton(
        text=title_btn_no, callback_data='reg_ntrpno')

    keyboard_builder.add(btn_yes)
    keyboard_builder.add(btn_no)
    keyboard_builder.adjust(2).as_markup()

    # way 2
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_btn_yes,
                              callback_data='reg_ntrpyes'),
         InlineKeyboardButton(text=title_btn_no, callback_data='reg_ntrpno')],
    ])
    return keyboard
    # return keyboard_builder.adjust(2).as_markup()


async def inline_ntrp_accept(chat_id):
    # way 2
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title.load_title(chat_id, 'reg_ntrp_btn_accept'),
                              callback_data='reg_ntrpyes'),],
    ])
    return keyboard
    # return keyboard_builder.adjust(2).as_markup()
