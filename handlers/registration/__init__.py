from aiogram import Router, Dispatcher
from handlers.registration import start
from handlers import callback
router_start = Router()
dp = Dispatcher()
start.run(router_start, dp)

# callback.run(router)
