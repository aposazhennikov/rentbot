'''
This function is making multi languages titles and store data for each users in json
'''

import json
import pathlib
from config import *
import re


# we should make class and __init__ here chat_id, I will do it later

def load_json():
    dir = pathlib.Path(__file__).parent.resolve()
    with open(f"{dir}/main.json", 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations


def load_title(chat_id, title_name, var=None):
    # lang is loading from config, but we should make in db or temp file for each users
    language = get_user_language(chat_id)
    translations = load_json()

    if language in translations and title_name in translations[language]:
        text_out = translations[language][title_name].get('text')

        # here is we can make loop but I dont see a reason for this now
        if var:
            text_out = re.sub('%var%', var, text_out)
        return text_out
    else:
        return None


def save_user_language(chat_id, lang):
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


def get_user_language(chat_id):
    dir = pathlib.Path(__file__).parent.resolve()
    file_path = f"{dir}/user_languages.json"

    if not pathlib.Path(file_path).exists():
        return None

    with open(file_path, "r") as file:
        data = json.load(file)

    language = data.get(str(chat_id))

    return language
