# Этот обработчик и функция вызываются из меню "Анкета" при нажатии "Пройти регистрацию сначала".
# Или командой edit_profile, если пользователь в базе данных -> запускаем процесс, иначе сообщение про /start.


@dp.message_handler(commands=['edit_profile'])
async def cmd_edit_profile(message: types.Message) -> None:
    pass
