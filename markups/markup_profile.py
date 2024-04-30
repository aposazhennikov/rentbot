# ------------------- Profile Menu -------------------
"""В будущем здесь будеть кнопка найти оппонента, 
когда мы реализуем функцию рейтинга"""

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from titles import title
from models.user import User


async def main_menu(chat_id):
    title_edit_profile = await title.load_title(chat_id, 'profile_btn_edit')
    title_delete_profile = await title.load_title(chat_id, 'profile_btn_delete')
    title_main_menu = await title.load_title(chat_id, 'title_main_menu')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_edit_profile,
                              callback_data=f'profile-edit'),
            InlineKeyboardButton(text=title_delete_profile, callback_data=f'profile-delete')],
        [InlineKeyboardButton(text=title_main_menu,
                              callback_data=f'main-menu')],
    ])

    return keyboard


async def edit_menu(chat_id):
    keyboard_builder = InlineKeyboardBuilder()
    user_manager = User(None)

    # structure = ['firstname', 'lastname', ... etc]
    structure = await user_manager.get_structure_profile_edit()

    # lets make inline buttons for each
    for item in structure:
        btn = InlineKeyboardButton(
            text=await title.load_title(chat_id, f'profile_btn_edit_{item}'), callback_data=f'profile-edit-{item}')
        keyboard_builder.add(btn)

    # button back to profile menu
    btn_back = InlineKeyboardButton(
        text=await title.load_title(chat_id, 'btn_back'), callback_data='profile-main')
    keyboard_builder.add(btn_back)

    keyboard_builder.adjust(2).as_markup()

    return keyboard_builder.adjust(2).as_markup()


async def delete_menu(chat_id):
    title_delete_yes = await title.load_title(chat_id, 'profile_btn_delete_yes')
    title_delete_no = await title.load_title(chat_id, 'profile_btn_delete_no')
    title_main_menu = await title.load_title(chat_id, 'title_main_menu')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title_delete_yes,
                              callback_data=f'profile-delete-confirm'),
            InlineKeyboardButton(text=title_delete_no, callback_data=f'profile-main')],
        [InlineKeyboardButton(text=title_main_menu,
                              callback_data=f'main-menu')],
    ])

    return keyboard
