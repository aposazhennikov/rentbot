# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

router_registration = Router()


@router_registration.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ''' NEED TO ADD DESCRIPTION '''
    await message.answer(text="here is a Alex's registration code")
