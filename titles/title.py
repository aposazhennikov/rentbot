import json
import pathlib
from config import *
import re


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
    # Получаем путь к текущему файлу и его родительскую директорию
    dir = pathlib.Path(__file__).parent.resolve()

    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    file_path = f"{dir}/user_languages.json"
    data = {}

    # Проверяем существует ли файл и загружаем данные
    if pathlib.Path(file_path).exists():
        with open(file_path, "r") as file:
            data = json.load(file)

    # Обновляем данные
    data[str(chat_id)] = lang

    # Записываем обновленные данные в файл
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_user_language(chat_id):
    # Получаем путь к текущему файлу и его родительскую директорию
    dir = pathlib.Path(__file__).parent.resolve()
    file_path = f"{dir}/user_languages.json"

    # Проверяем существует ли файл
    if not pathlib.Path(file_path).exists():
        return None

    # Загружаем данные из файла JSON
    with open(file_path, "r") as file:
        data = json.load(file)

    # Получаем язык пользователя по chat_id
    language = data.get(str(chat_id))

    return language
