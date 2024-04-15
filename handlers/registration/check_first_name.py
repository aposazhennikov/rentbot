# Хэндлер проверочный, чтобы отсечь "левые" имена, если наш FSM в первом режиме(first_name) следующие сообщения
# сначала проходят через этот обработчик. Сообщение проверку проходит: Если текст не длиннее 25 символов или не
# короче 3 символов, если сообщение состоит из букв одного алфавита(англи или русск)


@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=Registration.first_name)
async def check_first_name(message: types.Message):
    await message.reply("Введите настоящее имя!")
