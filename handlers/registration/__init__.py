from aiogram import Router
from handlers.registration import start

router = Router()

start.run(router)
