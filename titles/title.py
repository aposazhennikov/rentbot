import json
import pathlib
from config import *
import re


def load_json():
    dir = pathlib.Path(__file__).parent.resolve()
    with open(f"{dir}/main.json", 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations


def load_title(title_name, var=None):
    # lang is loading from config, but we should make in db or temp file for each users
    language = USER_LANGUAGE
    translations = load_json()

    if language in translations and title_name in translations[language]:
        text_out = translations[language][title_name].get('text')

        # here is we can make loop but I dont see a reason for this now
        if var:
            text_out = re.sub('%var%', var, text_out)
        return text_out
    else:
        return None
