# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from fsm.registration import Registration
from aiogram.fsm.context import FSMContext
from models.user import User
from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from handlers.registration import start
from titles import title


def run(dp):
    @dp.message(CommandStart())
    async def command_start_handler(message: Message, state: FSMContext) -> None:
        user_manager = User()
        get_user = user_manager.get_by_id(message.chat.id)

        if (get_user):
            message_out = title.load_title('welcome_back')
            await message.answer(f"{message_out}, {html.bold(get_user['first_name'])}!")
        else:
            message_out = title.load_title('reg_first_name')

            await message.answer(message_out)
            await state.set_state(Registration.first_name)

    @dp.message(Registration.first_name)
    async def reg_two(message: Message, state: FSMContext):
        await state.update_data(first_name=message.text)
        await state.set_state(Registration.last_name)

        message_out = title.load_title('reg_last_name')
        await message.answer(message_out)

    @dp.message(Registration.last_name)
    async def reg_three(message: Message, state: FSMContext):
        await state.update_data(last_name=message.text)
        data = await state.get_data()

        message_out = title.load_title('reg_finish')
        await message.answer(f"{message_out} " + html.bold(f"{data['first_name']} {data['last_name']}"))
        await state.clear()
