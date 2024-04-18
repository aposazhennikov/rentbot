from aiogram import Dispatcher
from handlers.registration import start

dp = Dispatcher()

start.run(dp)
