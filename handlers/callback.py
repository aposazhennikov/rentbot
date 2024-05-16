from aiogram import F
from aiogram.types import CallbackQuery
from aiogram import Router
from titles import title
from models.user import User
from aiogram.fsm.context import FSMContext
from fsm.menu import Menu
from handlers.court.court_callback import router_court_callback
import re

router_main_callback = Router()


@router_main_callback.callback_query(lambda c: re.match(r'main-', c.data))
async def handle_reg_callback(callback: CallbackQuery):
    split = callback.data.split('-')
    prefix, action = split
    await callback.answer(f'{prefix} {action}')
    print(f'{prefix} {action}')

    if (action == 'menu'):
        await callback.message.edit_text(text=await title.load_title(
            callback.message.chat.id, 'start_temp_menu'))
        pass


@router_main_callback.callback_query(lambda c: re.match(r'reg-', c.data))
async def handle_reg_callback(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    split = callback.data.split('-')
    prefix, action = split
    await callback.answer(f'{prefix} {action}')
    print(f'{prefix} {action}')

    if (action == 'temp'):
        # create user
        user_manager = User(chat_id)

        first_name = callback.from_user.first_name
        last_name = callback.from_user.last_name if callback.from_user.last_name != '' and callback.from_user.last_name is not None else callback.from_user.first_name
        params = {'first_name': first_name,
                  'last_name': last_name}

        if (callback.from_user.username):
            params['user_name'] = f'@{callback.from_user.username}'

        print(f'{params}')

        await user_manager.create(params)
        await callback.message.edit_text(text=await title.load_title(
            callback.message.chat.id, 'start_temp_menu'))
        pass
