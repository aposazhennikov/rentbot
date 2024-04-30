# Функция для изменения имени, выставляем наш FSM в first_name, приглашаем написать имя.
from titles import title
from markups import markup_registration, markup_lang
from models.user import User
from config import *
import time
import re
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from fsm.edit_profile import EditProfile
from titles import title
from aiogram import Router

router_profile_change_field = Router()


async def send_greetings_and_prompt_name(chat_id: int, field: str, callback: CallbackQuery = None, state: FSMContext = None):
    user_manager = User(chat_id)
    user_load = await user_manager.get_user_args(field)
    old_value = user_load[field]

    message_out = await title.load_title(chat_id, 'profile_change_field', await title.load_title(
        chat_id, f'title_field_{field}'), old_value)
    await callback.message.edit_text(message_out)

    # await state.set_state(EditProfile.field) #it doesnt work, i didnt find solution

    if (field == 'first_name'):
        await state.set_state(EditProfile.first_name)
    elif (field == 'last_name'):
        await state.set_state(EditProfile.last_name)
    elif (field == 'tennis_experience'):
        await state.set_state(EditProfile.tennis_experience)
    elif (field == 'ntrp'):
        await state.set_state(EditProfile.ntrp)
    elif (field == 'description'):
        await state.set_state(EditProfile.description)
    elif (field == 'phone_number'):
        await state.set_state(EditProfile.phone_number)
    elif (field == 'birth_day'):
        await state.set_state(EditProfile.birth_day)
    # we should add this to the state machine
    elif (field == 'gender'):
        await state.set_state(EditProfile.gender)


@router_profile_change_field.message(EditProfile.first_name)
async def reg_first_name(message: Message, state: FSMContext):
    string = await title.filter_symbols(message.text, 255, 'string')
    field_name = 'first_name'

    if len(string) > 2:
        await state.update_data(first_name=string)
        # data = await state.get_data()
        message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
        user_manager = User(message.chat.id)
        params = {field_name: str(string)}
        await user_manager.update(params)
        await message.answer(message_out)
        await state.clear()
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', string)
        await message.answer(message_out)
        await state.set_state(EditProfile.first_name)


@router_profile_change_field.message(EditProfile.last_name)
async def reg_first_name(message: Message, state: FSMContext):
    string = await title.filter_symbols(message.text, 255, 'string')
    field_name = 'last_name'

    if len(string) > 2:
        await state.update_data(last_name=string)
        # data = await state.get_data()
        message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
        user_manager = User(message.chat.id)
        params = {field_name: str(string)}
        await user_manager.update(params)
        await message.answer(message_out)
        await state.clear()
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', string)
        await message.answer(message_out)
        await state.set_state(EditProfile.last_name)

'''
@router_profile_change_field.message(Registration.last_name)
async def reg_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.tennis_experience)
    data = await state.get_data()
    message_out = title.load_title(message.chat.id, 'reg_tennis_experience',
                                   str(f"{data['first_name']} {message.text}"))
    await message.answer(message_out)


@router_profile_change_field.message(Registration.tennis_experience)
async def reg_ntrp_quest(message: Message, state: FSMContext):
    await state.update_data(tennis_experience=message.text)
    message_out = title.load_title(
        message.chat.id, 'reg_ntrp_quest', message.text)
    await message.answer(message_out,  reply_markup=await markup_registration.inline_ntrp_quest(message.chat.id))


@router_profile_change_field.callback_query(lambda c: re.match(r'reg_ntrp', c.data))
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


@router_profile_change_field.message(Registration.ntrp)
async def reg_finish(message: Message, state: FSMContext):
    await state.update_data(ntrp=message.text)
    data = await state.get_data()
    message_out = f"{title.load_title(message.chat.id, 'reg_finish')}\n"

    message_out += "\n".join(f"<b>{key}</b> = {value}" for key,
                             value in data.items())

    await message.answer(message_out)
    await state.clear()
'''
