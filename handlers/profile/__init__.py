from aiogram import Router
from handlers.profile import profile_main
from handlers import callback
router_profile = Router()

profile_main.run(router_profile)
