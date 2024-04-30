import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import *
from handlers.registration import router_registration
from handlers.help import router_help
from handlers.profile.profile_main import router_profile
from handlers.profile.profile_callback import router_profile_callback
from handlers.profile.change_field import router_profile_change_field
from handlers.callback import router_main_callback
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

    # ===== REGISTRATION/START BLOCK =====
    dp.include_router(router_registration)

    # ===== PROFILE BLOCK =====
    # main router with buttons edit delete
    dp.include_router(router_profile)
    # callbacks for profile
    dp.include_router(router_profile_callback)
    # FSM for profile edit
    router_profile_callback.include_router(router_profile_change_field)

    # ===== HELP BLOCK =====
    # change language + callback there
    dp.include_router(router_help)

    # ===== MAIN MENU BLOCK =====
    dp.include_router(router_main_callback)

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        # All handlers should be attached  to the Router (or Dispatcher)

    except KeyboardInterrupt:
        print('Break')
