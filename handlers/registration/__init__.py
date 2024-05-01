# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.methods.send_contact import SendContact
# temp
from titles import title

router_registration = Router()


@router_registration.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ''' NEED TO ADD DESCRIPTION '''
    await message.answer(text="here is registration")

    # temp code main menu
    await message.answer(text=await title.load_title(message.chat.id, 'start_temp_menu'))
