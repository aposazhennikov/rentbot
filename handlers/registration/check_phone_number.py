# Хэндлер проверочный, чтобы отсечь "левые" номера, если наш FSM в режиме (phone_number) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра равна нулю или
# если прошел проверку регулярным выражением regular_number из файла config.

# Тут конечно нужно все менять...

@dp.message_handler(lambda message: not message.text.isdigit() or (
    float(message.text) != 0 and not re.match(regular_number, message.text)),
    state=Registration.phone_number)
async def check_phone_number(message: types.Message):
    pass
