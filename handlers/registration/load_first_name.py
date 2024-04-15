# Если наш FSM в первом режиме(first_name) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "first_name", переключает FSM в следующий режим(last_name) Отправляет приглашающее сообщения для ввода фамилии.

@dp.message_handler(state=Registration.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    pass
