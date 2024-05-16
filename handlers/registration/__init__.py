# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
# temp
from titles import title
from models.user import User
from markups import markup_registration

router_registration = Router()


@router_registration.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ''' NEED TO ADD DESCRIPTION '''
    chat_id = message.chat.id
    user_lang = await title.get_user_language(chat_id)

    if (user_lang is None):
        await message.answer(text='/help Выбери свой язык (Choose your language)')

    else:
        user_manager = User(chat_id)
        user_load = await user_manager.get()

        if user_load is None:
            print(f'user is newbie')

            photo_id = 'CAACAgIAAxkBAAIG_mYicDef3ift5VHRRBmffs0fwRrcAAJqEwAC3tAAAUjVScbwz0Wt9zQE'
            await message.bot.send_animation(chat_id, photo_id)
            await message.answer(text=await title.load_title(chat_id, 'reg_temp_asc'), reply_markup=await markup_registration.registration_temp(chat_id))
        else:
            print(f'user is load')
            # temp code main menu
            await message.answer(text=await title.load_title(message.chat.id, 'start_temp_menu'))
