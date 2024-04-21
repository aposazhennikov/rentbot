# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.
from fsm.registration import Registration
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import re
import time

# Bot token & DB parametres
from config import *

# Class User has methods __init__ which making connect to DB, get_user_args, get_by_id, create, update, delete, get_all
# Class has working with DB purposes
from models.user import User

# Markup_registration has inline_ntrp_quest & inline_ntrp_accept methods, which input chat_id and returns keyboards with btns
# Markup_lang has reply_lang which returns keyboards with lang choose en/ru
from markups import markup_registration, markup_lang

# Contains load_json, load_title, save_user_language methods which works with translation list of main phrases
from titles import title


TITLE_CHOICE = "Выбери язык (Choose a language):"


@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(TITLE_CHOICE, reply_markup=await markup_lang.reply_lang())


async def send_greetings_and_prompt_name(chat_id: int, message: Message = None, callback: CallbackQuery = None, state: FSMContext = None):
    user_language = title.get_user_language(chat_id)
    if user_language is None:
        markup = await markup_lang.reply_lang()
        if message:
            await message.answer(TITLE_CHOICE, reply_markup=markup)
        elif callback:
            await callback.message.answer(TITLE_CHOICE, reply_markup=markup)
    else:
        user_manager = User()
        get_user = user_manager.get_user_args(chat_id, 'first_name')

        if get_user and BOT_MODE != 'dev':
            message_out = title.load_title(
                chat_id, 'start_greetings', get_user['first_name'])
            if message:
                await message.answer(message_out)
            elif callback:
                await callback.message.edit_text(message_out)
        else:
            if get_user:
                message_dev = f"DEV MODE. Hey {
                    get_user['first_name']} 😉 you didnt see this, okay ?"
                if message:
                    await message.answer(message_dev)
                elif callback:
                    await callback.message.answer(message_dev)

            message_out = title.load_title(
                chat_id, 'start_greetings_first')
            message_out_reg_fn = title.load_title(
                chat_id, 'reg_first_name')
            if message:
                await message.answer(message_out)
                time.sleep(2)
                await message.answer(message_out_reg_fn)
            elif callback:
                await callback.message.edit_text(message_out)
                time.sleep(2)
                await callback.message.answer(message_out_reg_fn)
            await state.set_state(Registration.first_name)


@router.message(CommandStart())
async def command_help_handler(message: Message, state: FSMContext) -> None:
    await send_greetings_and_prompt_name(message.chat.id, message=message, state=state)


@router.callback_query(lambda c: re.match(r'lang_', c.data))
async def reg_ntrp(callback: CallbackQuery, state: FSMContext):
    split = callback.data.split('_')
    prefix, lang = split
    if lang:
        title.save_user_language(callback.message.chat.id, lang)
    await send_greetings_and_prompt_name(callback.message.chat.id, callback=callback, state=state)


@router.message(Registration.first_name)
async def reg_first_name(message: Message, state: FSMContext):
    await state.set_state(Registration.last_name)
    await state.update_data(first_name=message.text)
    message_out = title.load_title(
        message.chat.id, 'reg_last_name', message.text)
    await message.answer(message_out)


@router.message(Registration.last_name)
async def reg_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.tennis_experience)
    data = await state.get_data()
    message_out = title.load_title(message.chat.id, 'reg_tennis_experience',
                                   str(f"{data['first_name']} {message.text}"))
    await message.answer(message_out)


@router.message(Registration.tennis_experience)
async def reg_ntrp_quest(message: Message, state: FSMContext):
    await state.update_data(tennis_experience=message.text)
    message_out = title.load_title(
        message.chat.id, 'reg_ntrp_quest', message.text)
    await message.answer(message_out,  reply_markup=await markup_registration.inline_ntrp_quest(message.chat.id))


@router.callback_query(lambda c: re.match(r'reg_ntrp', c.data))
async def reg_ntrp(callback: CallbackQuery, state: FSMContext):
    split = callback.data.split('_')
    prefix, action = split
    await callback.answer(action)

    # No hardcode more PLS
    if action == 'ntrpyes':
        message_out = title.load_title(
            callback.message.chat.id, 'reg_ntrp_yes')
        await callback.message.edit_text(message_out, reply_markup=None)
        await state.set_state(Registration.ntrp)

        # No hardcode more PLS
    elif action == 'ntrpno':
        message_out = title.load_title(
            callback.message.chat.id, 'reg_ntrp_no')
        await callback.message.edit_text(message_out,
                                         reply_markup=await markup_registration.inline_ntrp_accept(callback.message.chat.id))


@router.message(Registration.ntrp)
async def reg_finish(message: Message, state: FSMContext):
    await state.update_data(ntrp=message.text)
    data = await state.get_data()
    message_out = f"{title.load_title(message.chat.id, 'reg_finish')}\n"
    message_out += "\n".join(f"<b>{key}</b> = {value}" for key,
                             value in data.items())

    await message.answer(message_out)
    await state.clear()
