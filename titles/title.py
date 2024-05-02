'''
This function is making multi languages titles and store data for each users in json
'''

import json
import pathlib
import re
from config import *


# we should make class and __init__ here chat_id, I will do it later
async def load_json():
    '''
    Function return loaded file with different locales
    This locales contains phrases on different languages, for example:

    EN start_greetings_first: Hi, Im bot <b>Rafa</b>! Lets make your profile.
    RU start_greetings_first: Привет. Меня зовут бот Рафа и я буду твоим проводником и помощником по теннисным тренировкам на корте в Овсянниковском саду.
    '''
    dir = pathlib.Path(__file__).parent.resolve()
    with open(f"{dir}/main.json", 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations


async def load_title(chat_id, title_name, *args):
    '''
    Function takes as input CHAT_ID - this shows us user and TITLE_NAME from loaded JSON,
    and VAR - this is value, which we can change in TEXT 
    Function RETURN text from TITLE_NAME, for example:

     TITLE_NAME:"reg_tennis_experience": {
            TEXT: "Super, <b>%var%</b>, nice to meet you!"}

    '''
    # language is loading from config, but we should make in db or temp file for each users
    language = await get_user_language(chat_id)
    translations = await load_json()

    if language in translations and title_name in translations[language]:
        text_out = translations[language][title_name].get('text')
        # Changing %var% in our string to value, which we get from "var"
        for arg in args:
            if arg is None or arg == 'None':
                # print('old_value is None')
                arg = translations[language]['system_title_none'].get('text')
            text_out = text_out.replace('%var%', arg, 1)

        return text_out
    else:
        return f"Unknown {title_name}"


async def save_user_language(chat_id, lang):
    dir = pathlib.Path(__file__).parent.resolve()
    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    file_path = f"{dir}/user_languages.json"
    data = {}
    if pathlib.Path(file_path).exists():
        with open(file_path, "r") as file:
            data = json.load(file)

    data[str(chat_id)] = lang

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


async def get_user_language(chat_id):
    dir = pathlib.Path(__file__).parent.resolve()
    file_path = f"{dir}/user_languages.json"

    if not pathlib.Path(file_path).exists():
        return None

    with open(file_path, "r") as file:
        data = json.load(file)

    language = data.get(str(chat_id))

    return language


# filter symbols float string any
async def filter_symbols(string, max_len=255, type='any', reg=None):
    if reg is not None:
        pattern = re.compile(reg)
        if not re.match(pattern, string):
            return False

    if (type == 'float'):
        string = string.replace(',', '.')
        set_chars = set('0123456789.,')
    elif (type == 'string'):
        set_chars = set(
            'ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёйцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- ')
    else:
        set_chars = set(
            'ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёйцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%!,.(),._- ')

    if len(string) > int(max_len):
        string = string[:max_len]

    string = str(
        ''.join(symbol if symbol in set_chars else '' for symbol in string))
    return string
