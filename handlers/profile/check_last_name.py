# Проверочный хэндлер идентичный тому, что был при регистрации, только FSM он принимает не из класса Registration,
# а из класса EditProfile.
@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=EditProfile.last_name)
async def check_last_name(message: types.Message):
    await message.reply("Введи настоящую фамилию!")
