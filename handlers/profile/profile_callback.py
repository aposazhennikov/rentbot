from aiogram import F
from aiogram.types import CallbackQuery
from aiogram import Router
from markups import markup_profile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.profile.profile_main import get_profile_info
from titles import title
import re

# Functions: run, command_help_handler, send_greetings_and_prompt_name, reg_ntrp, reg_first_name, reg_last_name,  reg_ntrp_quest, reg_ntrp, reg_ntrp
from handlers.registration import start
from models.user import User
router_profile_callback = Router()


''' NEED TO ADD DESCRIPTION '''
# Тут бы пояснения что лямбда делает...
# lambda c это c= callback, где мы c.data из этого вытаскиваем и проверяем начинается ли они с префикса нам нужного


@router_profile_callback.callback_query(lambda c: re.match(r'profile-', c.data))
async def handle_profile_callback(callback: CallbackQuery):
    split = callback.data.split('-')
    print(split)

    if len(split) == 2:
        prefix, action = split
        await callback.answer(action)

        if (action == 'edit'):
            body = await profile_callback_main(action, callback.message.chat.id)
            await callback.message.edit_text(text=body, reply_markup=await markup_profile.edit_menu(callback.message.chat.id))
        else:
            body = await profile_callback_main(action, callback.message.chat.id)
            await callback.message.edit_text(text=body, reply_markup=await markup_profile.main_menu(callback.message.chat.id))

    # here is fields edit callback looks like: ['profile', 'edit', 'first_name']
    elif len(split) == 3:
        prefix, action, field = split

        await callback.answer(f'{action} {field}')
    #
    else:
        print(f'count: {len(split)}')


async def profile_callback_main(action, chat_id):
    print(f"{action} : {chat_id}")

    if action == 'edit':
        return await title.load_title(chat_id, 'profile_title_edit')
        pass
    elif action == 'delete':
        return f"{action} : {chat_id}"
        # code delete profile
        pass
    elif action == 'main':
        user_manager = User()
        user_load = await user_manager.get_by_id(chat_id)
        message_out = await get_profile_info(chat_id, user_load)
        return message_out
