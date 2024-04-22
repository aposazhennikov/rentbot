import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import *
from handlers.registration import router_start
from handlers.profile import router_profile
from logs import rent_logger

# file and console loger $path:/logs/errors.log
# this makes the bot slower
if BOT_MODE == 'dev':
    rent_logger.run()
dp = Dispatcher()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    # Connect router from handlers
    dp.include_router(router_start)
    dp.include_router(router_profile)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        # All handlers should be attached  to the Router (or Dispatcher)

    except KeyboardInterrupt:
        print('Break')
