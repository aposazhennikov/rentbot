from aiogram import F
from aiogram.types import CallbackQuery
from handlers.registration import start
import re


def run(router):
    @router.callback_query(lambda c: re.match(r'reg_', c.data))
    async def handle_reg_callback(callback: CallbackQuery):
        split = callback.data.split('_')
        prefix, action = split
        # print(split)
        await callback.answer('OK')
        start.reg_ntrp(callback)
