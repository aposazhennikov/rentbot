from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


async def reply_lang():
    ''' NEED TO ADD DESCRIPTION OF THIS FUNCTION '''
    # way 1
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Русский', callback_data='lang-ru'),
        InlineKeyboardButton(text='English', callback_data='lang-en')]])
    return keyboard
