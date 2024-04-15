# Хэндлер для обработки функции "Изменить имя" в цепочке меню "анкета"
# Если FSM стоит в first_name и предыдущий хэндлер пройден -> заменить в базе данных имя на текст сообщения,
# отправить сообщение об изменении, завершить FSM, отправить пользователю его профиль(ф-ция из main_menu)
@dp.message_handler(state=EditProfile.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    pass
