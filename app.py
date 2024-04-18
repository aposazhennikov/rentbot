import asyncio
import pathlib
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import *

# path log settings
dir = pathlib.Path(__file__).parent.resolve()
directory_path = pathlib.Path(f'{dir}/logs')
if not directory_path.exists():
    directory_path.mkdir(parents=True, exist_ok=True)

# settings logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# file logger
file_handler = logging.FileHandler(f'{directory_path}/errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# run logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# All handlers should be attached  to the Router (or Dispatcher)
if BOT_TOKEN:
    dp = Dispatcher()

    async def main() -> None:
        # Initialize Bot instance with default bot properties which will be passed to all API calls
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))
        # And the run events dispatching
        await dp.start_polling(bot)

    if __name__ == "__main__":
        from handlers.registration import *
        asyncio.run(main())
else:
    print('BOT_TOKEN is not set')
