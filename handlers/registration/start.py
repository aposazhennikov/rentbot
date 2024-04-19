# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from fsm.registration import Registration
from aiogram.fsm.context import FSMContext
from models.user import User
from aiogram import types, html

from aiogram.filters import CommandStart
from aiogram.types import Message
from titles import title

import time


def run(router):
    @router.message(CommandStart())
    async def command_start_handler(message: Message, state: FSMContext) -> None:
        user_manager = User()
        # similar funciton, i imported #get_db_args from old and modified it
        # get_user = user_manager.get_by_id(message.chat.id)
        get_user = user_manager.get_user_args(
            message.chat.id, 'first_name')

        if (get_user):
            message_out = title.load_title(
                'start_greetings', get_user['first_name'])
            await message.answer(message_out)

            # show menu here
        else:
            message_out_greetings = title.load_title('start_greetings_first')
            message_out_reg_fn = title.load_title('reg_first_name')

            await message.answer(message_out_greetings)
            time.sleep(2)
            await message.answer(message_out_reg_fn)
            await state.set_state(Registration.first_name)

    @router.message(Registration.first_name)
    async def reg_first_name(message: Message, state: FSMContext):
        await state.update_data(first_name=message.text)
        await state.set_state(Registration.last_name)

        message_out = title.load_title('reg_last_name', message.text)
        await message.answer(message_out)

    @router.message(Registration.last_name)
    async def reg_last_name(message: Message, state: FSMContext):
        await state.update_data(last_name=message.text)
        await state.set_state(Registration.tennis_experience)

        message_out = title.load_title('reg_tennis_experience', message.text)
        await message.answer(message_out)


'''
    @dp.message(Registration.finish)
    async def reg_ln(message: Message, state: FSMContext):
        await state.update_data(last_name=message.text)
        data = await state.get_data()

        message_out = title.load_title('reg_finish')
        await message.answer(f"{message_out} " + html.bold(f"{data['first_name']} {data['last_name']}"))
        await state.clear()
'''
