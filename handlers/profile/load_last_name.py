# Если FSM стоит в last_name и предыдущий хэндлер пройден -> заменить в базе данных фамилию на текст сообщения,
# отправить сообщение об изменении, завершить FSM, отправить пользователю его профиль(ф-ция из main_menu)
@dp.message_handler(state=EditProfile.last_name)
async def load_last_name(message: types.Message, state: FSMContext) -> None:
    pass