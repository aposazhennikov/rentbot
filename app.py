import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import *
from handlers.registration import router
from logs import rent_logger

rent_logger.run()

# All handlers should be attached  to the Router (or Dispatcher)
if BOT_TOKEN:
    dp = Dispatcher()

    async def main() -> None:
        # Initialize Bot instance with default bot properties which will be passed to all API calls
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))
        # Connect router from handlers
        dp.include_router(router)
        # And the run events dispatching
        await dp.start_polling(bot)

    if __name__ == "__main__":
        # from handlers.registration import *
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print('Break')
else:
    print('BOT_TOKEN is not set')
