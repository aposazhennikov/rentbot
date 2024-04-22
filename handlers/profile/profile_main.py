from models.user import User
from markups import markup_profile
from aiogram.filters import Command
from aiogram.types import Message
from titles import title
from config import *


def run(router):
    @router.message(Command('profile'))
    async def command_profile_handler(message: Message) -> None:
        user_manager = User()
        user_load = user_manager.get_by_id(message.chat.id)

        if (user_manager):
            message_out = title.load_title(
                message.chat.id, 'profile_main_menu', user_load['first_name'])
            await message.answer(message_out, reply_markup=await markup_profile.main_menu(message.chat.id))
