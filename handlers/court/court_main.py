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
        await message.bot.send_message(BOT_GROUP_ID, f'user {message.chat.id} watching court', BOT_TOPIC_ID)
        await message.answer(await title.load_title(message.chat.id, 'court_main'), reply_markup=await markup_court.main_menu(message.chat.id))
    else:
        # run registration
        await message.answer('u should reg')
