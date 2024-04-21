from aiogram import F
from aiogram.types import CallbackQuery
import re


# Functions: run, command_help_handler, send_greetings_and_prompt_name, reg_ntrp, reg_first_name, reg_last_name,  reg_ntrp_quest, reg_ntrp, reg_ntrp
from handlers.registration import start



# Тут бы пояснения что лямбда делает...
@router.callback_query(lambda c: re.match(r'reg_', c.data))
async def handle_reg_callback(callback: CallbackQuery):
    ''' NEED TO ADD DESCRIPTION '''
    split = callback.data.split('_')
    prefix, action = split
    await callback.answer('OK')
    start.reg_ntrp(callback)
