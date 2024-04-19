from aiogram import Dispatcher, Router
from handlers.registration import start

router = Router()

start.run(router)
