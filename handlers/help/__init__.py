from aiogram import Router

from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import re

# Bot token & DB parametres
from config import *

# Markup_registration has inline_ntrp_quest & inline_ntrp_accept methods, which input chat_id and returns keyboards with btns
# Markup_lang has reply_lang which returns keyboards with lang choose en/ru
from markups import markup_lang

# Contains load_json, load_title, save_user_language methods which works with translation list of main phrases
from titles import title


TITLE_CHOICE = "Выбери язык (Choose a language):"


router_help = Router()


@router_help.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    ''' NEED TO ADD DESCRIPTION '''
    await message.answer(TITLE_CHOICE, reply_markup=await markup_lang.reply_lang())


@router_help.callback_query(lambda c: re.match(r'lang-', c.data))
async def reg_ntrp(callback: CallbackQuery, state: FSMContext):
    ''' NEED TO ADD DESCRIPTION '''
    split = callback.data.split('-')
    prefix, lang = split

    if lang:
        await title.save_user_language(callback.message.chat.id, lang)
        await callback.message.edit_text(text=await title.load_title(
            callback.message.chat.id, 'start_temp_menu'))
        # await send_greetings_and_prompt_name(callback.message.chat.id, callback=callback, state=state)
