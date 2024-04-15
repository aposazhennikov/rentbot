# Хэндлер проверочный, чтобы отсечь "левый" возраст, если наш FSM в режиме (age) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра меньше ста, но
# больше четырех.


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100 or float(message.text) < 4,
                    state=Registration.age)
async def check_age(message: types.Message):
    await message.reply('Введи реальный возраст!')
