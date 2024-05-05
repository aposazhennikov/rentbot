from aiogram import Router
from handlers.registration import start
from handlers import callback
router_start = Router()

start.run(router_start)

# callback.run(router)
