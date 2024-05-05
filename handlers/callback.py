from aiogram import F
from aiogram.types import CallbackQuery
from aiogram import Router
from titles import title
import re

router_main_callback = Router()

''' NEED TO ADD DESCRIPTION '''
# Тут бы пояснения что лямбда делает...


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
