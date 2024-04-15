# Если наш FSM в режиме(last_name) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "last_name", переключает FSM в следующий режим(age) Отправляет приглашающее сообщения для ввода возраста.


@dp.message_handler(state=Registration.last_name)
async def load_last_name(message: types.Message, state: FSMContext) -> None:
    pass
