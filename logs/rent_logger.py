import logging
import pathlib


def run():
    # path log settings
    dir = pathlib.Path(__file__).parent.resolve()

    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    # settings logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # file logger
    file_handler = logging.FileHandler(f'{dir}/errors.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    # run logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
