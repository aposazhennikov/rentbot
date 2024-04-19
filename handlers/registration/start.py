# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from fsm.registration import Registration
from aiogram.fsm.context import FSMContext
from models.user import User
from aiogram import types, html
from markups import markup_registration
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from titles import title
import re
import time


def run(router):
    @router.message(CommandStart())
    async def command_start_handler(message: Message, state: FSMContext) -> None:
        await state.update_data(tennis_experience=message.text)
        await state.set_state(Registration.ntrp_quest)

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
        data = await state.get_data()
        message_out = title.load_title(
            'reg_tennis_experience', str(f"{data['first_name']} {message.text}"))
        await message.answer(message_out)

    @router.message(Registration.tennis_experience)
    async def reg_ntrp_quest(message: Message, state: FSMContext):
        await state.update_data(tennis_experience=message.text)
        # await state.set_state(Registration.ntrp_quest)

        message_out = title.load_title('reg_ntrp_quest', message.text)
        await message.answer(message_out,  reply_markup=await markup_registration.inline_ntrp_quest())

    @router.callback_query(lambda c: re.match(r'reg_ntrp', c.data))
    async def reg_ntrp(callback: CallbackQuery, state: FSMContext):
        split = callback.data.split('_')
        prefix, action = split
        await callback.answer(action)
        # await state.update_data(ntrp_quest=action)

        if action == 'ntrpyes':
            message_out = title.load_title('reg_ntrp_yes')
            await callback.message.edit_text(message_out, reply_markup=None)
            await state.set_state(Registration.ntrp)
        elif action == 'ntrpno':
            message_out = title.load_title('reg_ntrp_no')
            await callback.message.edit_text(message_out, reply_markup=await markup_registration.inline_ntrp_accept())

    @router.message(Registration.ntrp)
    async def reg_finish(message: Message, state: FSMContext):
        await state.update_data(ntrp=message.text)
        data = await state.get_data()
        message_out = f"{title.load_title('reg_finish')}\n"

        message_out += "\n".join(f"<b>{key}</b> = {value}" for key,
                                 value in data.items())

        await message.answer(message_out)
        await state.clear()


'''
    @dp.message(Registration.finish)
    async def reg_ln(message: Message, state: FSMContext):
        await state.update_data(last_name=message.text)
        data = await state.get_data()

        message_out = title.load_title('reg_finish')
        await message.answer(f"{message_out} " + html.bold(f"{data['first_name']} {data['last_name']}"))
        await state.clear()
'''
