if __name__ == '__main__':
    from handlers.registration import *
    executor.start_polling(dp, skip_updates=True)