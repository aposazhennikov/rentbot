from aiogram import Router
from handlers.registration import start
from handlers import callback
router = Router()

start.run(router)

# callback.run(router)
