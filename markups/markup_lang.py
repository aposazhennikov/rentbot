from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


async def reply_lang():
    # way 1
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Русский',
                              callback_data='lang_ru'),
         InlineKeyboardButton(text='English', callback_data='lang_en')],
    ])
    return keyboard
