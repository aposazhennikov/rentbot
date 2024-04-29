from aiogram import F
from aiogram.types import CallbackQuery
import re
from aiogram import Router

# Functions: run, command_help_handler, send_greetings_and_prompt_name, reg_ntrp, reg_first_name, reg_last_name,  reg_ntrp_quest, reg_ntrp, reg_ntrp
from handlers.registration import start
router_profile_callback = Router()


''' NEED TO ADD DESCRIPTION '''
# Тут бы пояснения что лямбда делает...


@router_profile_callback.callback_query(lambda c: re.match(r'profile_', c.data))
async def handle_profile_callback(callback: CallbackQuery):
    split = callback.data.split('_')
    prefix, action = split
    await callback.answer(action)
    body = profile_callback_main(action, callback.message.chat.id)
    await callback.message.edit_text(text=body, reply_markup=None)


def profile_callback_main(action, chat_id):
    print(f"{action} : {chat_id}")

    if action == 'edit':
        return f"{action} : {chat_id}"
        # code edit profile
        pass
    elif action == 'delete':
        return f"{action} : {chat_id}"
        # code delete profile
        pass
