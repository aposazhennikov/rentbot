import json
import pathlib
from config import *


def load_json():
    dir = pathlib.Path(__file__).parent.resolve()
    with open(f"{dir}/main.json", 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations


def load_title(title_name):
    language = USER_LANGUAGE
    translations = load_json()

    if language in translations and title_name in translations[language]:
        return translations[language][title_name].get('text')
    else:
        return None
