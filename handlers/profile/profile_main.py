from models.user import User
from markups import markup_profile
from aiogram.filters import Command
from aiogram.types import Message
from titles import title
from config import *
from aiogram import Router

router_profile = Router()


@router_profile.message(Command('profile'))
async def command_profile_handler(message: Message) -> None:
    user_manager = User(message.chat.id)
    user_load = await user_manager.get()

    if (user_load):
        message_out = await get_profile_info(message.chat.id, user_load)
        await message.answer(message_out, reply_markup=await markup_profile.main_menu(message.chat.id))
    else:
        await message.answer('u should reg')


async def get_profile_info(chat_id, user_load):
    # we have to check and print each field if it exists in order. but now from TT

    out = await title.load_title(chat_id, 'profile_main_menu')
    user_manager = User(chat_id)
    fields = await user_manager.get_fields_profile()

    for field in fields:
        if (user_load[field] != None):
            if field == 'gender':
                if user_load[field] == 'male':
                    field_value = "🚹"
                elif user_load[field] == 'female':
                    field_value = "🚺"
                else:
                    field_value = user_load[field]
            else:
                field_value = user_load[field]
            title_field = await title.load_title(chat_id, f'title_field_{field}')
            capitalized_word = title_field[0].upper() + title_field[1:]
            out += f'<b>{capitalized_word}</b> : {field_value}\n'
    return out
