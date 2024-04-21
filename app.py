import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_MODE, BOT_TOKEN
from handlers.registration import router
from logs import rent_logger

# file and console loger $path:/logs/errors.log
# this makes the bot slower
if BOT_TOKEN:
    dp = Dispatcher()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # Connect router from handlers All handlers should be attached  to the Router (or Dispatcher)
    # And the run events dispatching
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        if BOT_MODE == "dev":
            rent_logger.run()
        else:
            print("BOT_TOKEN is not set")

    except KeyboardInterrupt:
        print("Break")
