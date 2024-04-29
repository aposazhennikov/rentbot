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
    user_manager = User()
    user_load = user_manager.get_by_id(message.chat.id)

    if (user_load):
        if (user_load['user_name'] == None):
            message_out = title.load_title(
                message.chat.id, 'profile_main_menu_with_username',
                user_load['first_name'], user_load['last_name'], user_load['birth_day'],
                user_load['ntrp'], user_load['tennis_experience'],
                user_load['phone_number'], user_load['description'])
        else:
            message_out = title.load_title(
                message.chat.id, 'profile_main_menu_without_username',
                user_load['first_name'], user_load['last_name'], user_load['birth_day'],
                user_load['ntrp'], user_load['tennis_experience'], user_load['user_name'],
                user_load['phone_number'], user_load['description'])

        await message.answer(message_out, reply_markup=await markup_profile.main_menu(message.chat.id))
