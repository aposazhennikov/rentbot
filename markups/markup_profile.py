# ------------------- Profile Menu -------------------
"""В будущем здесь будеть кнопка найти оппонента, 
когда мы реализуем функцию рейтинга"""

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from titles import title


async def main_menu(chat_id):
    # way 1
    title_edit_profile = title.load_title(chat_id, 'profile_btn_edit')
    title_delete_profile = title.load_title(chat_id, 'profile_btn_delete')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_edit_profile,
                              callback_data=f'profile_edit_{chat_id}'),
            InlineKeyboardButton(text=title_delete_profile, callback_data=f'profile_delete_{chat_id}')],
    ])

    return keyboard
