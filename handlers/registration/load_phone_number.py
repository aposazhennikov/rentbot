# Если наш FSM в режиме(phone_number) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "age", переключает FSM в следующий режим(photo) Отправляет приглашающее сообщения для отправки фотографии.

@dp.message_handler(state=Registration.phone_number)
async def load_phone_number(message: types.Message, state: FSMContext) -> None:
    pass
