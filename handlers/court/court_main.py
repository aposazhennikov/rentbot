from models.user import User
from markups import markup_court
from aiogram.filters import Command
from aiogram.types import Message
from titles import title
from config import *
from aiogram import Router

router_court = Router()


@router_court.message(Command('court'))
async def command_court_handler(message: Message) -> None:
    user_manager = User(message.chat.id)
    user_load = await user_manager.get()

    if (user_load):
        # message_out = await get_court_menu(message.chat.id, user_load)

        await message.answer(await title.load_title(message.chat.id, 'court_main'), reply_markup=await markup_court.main_menu(message.chat.id))
    else:
        # run registration
        await message.answer('u should reg')


async def get_court_menu(chat_id, user_load):
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
