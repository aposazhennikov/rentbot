# Функция для изменения имени, выставляем наш FSM в first_name, приглашаем написать имя.
from titles import title
from models.user import User
from config import *
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from fsm.edit_profile import EditProfile
from titles import title
from aiogram import Router
from handlers.profile import profile_main
from markups import markup_profile
import re

router_profile_change_field = Router()


async def send_greetings_and_prompt_name(chat_id: int, field: str, callback: CallbackQuery = None, state: FSMContext = None):
    user_manager = User(chat_id)
    user_load = await user_manager.get_user_args(field)
    if field == 'gender':
        if user_load[field] == 'male':
            old_value = "🚹"
        elif user_load[field] == 'female':
            old_value = "🚺"
        else:
            old_value = user_load[field]
    else:
        old_value = user_load[field]

    message_out = await title.load_title(chat_id, 'profile_change_field', await title.load_title(
        chat_id, f'title_field_{field}'), old_value)

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
        # share_contact here
        await callback.message.answer(text=await title.load_title(chat_id, 'profile_title_share_phone'), reply_markup=await markup_profile.share_contact(chat_id))
        await state.set_state(EditProfile.phone_number)
    elif (field == 'birth_day'):
        await state.set_state(EditProfile.birth_day)
    elif (field == 'gender'):
        await callback.message.answer(text=await title.load_title(chat_id, 'profile_title_choice_gender'), reply_markup=await markup_profile.choice_gender(chat_id))
        await state.set_state(EditProfile.gender)

    await callback.message.edit_text(message_out)


@router_profile_change_field.message(EditProfile.first_name)
async def edit_first_name(message: Message, state: FSMContext):
    field_name = 'first_name'

    if message.text:
        string = await title.filter_symbols(message.text, 255, 'string')

        if string is not False and len(string) > 2:
            await state.update_data(first_name=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', string)
            await message.answer(message_out)
            await state.set_state(EditProfile.first_name)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.first_name)


@router_profile_change_field.message(EditProfile.last_name)
async def edit_last_name(message: Message, state: FSMContext):
    field_name = 'last_name'

    if message.text:
        string = await title.filter_symbols(message.text, 255, 'string')

        if string is not False and len(string) > 2:
            await state.update_data(last_name=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', string)
            await message.answer(message_out)
            await state.set_state(EditProfile.last_name)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.last_name)


@router_profile_change_field.message(EditProfile.ntrp)
async def edit_ntrp(message: Message, state: FSMContext):
    field_name = 'ntrp'

    if message.text:
        # regular expression
        reg = '^([1-6]|[1-6][\.,][\d?]+|7)$'
        string = await title.filter_symbols(message.text, 3, 'float', reg)

        if string is not False and len(string) > 0:
            await state.update_data(ntrp=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', message.text)
            await message.answer(message_out)
            await state.set_state(EditProfile.ntrp)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.ntrp)


@router_profile_change_field.message(EditProfile.birth_day)
async def edit_birth_day(message: Message, state: FSMContext):
    field_name = 'birth_day'

    if message.text:
        # regular expression
        # reg = '(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d'
        reg = '(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d'
        string = await title.filter_symbols(str(message.text), 10, 'any', reg)

        if string is not False and len(string) > 0:
            await state.update_data(birth_day=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', message.text)
            await message.answer(message_out)
            await state.set_state(EditProfile.birth_day)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.birth_day)


@router_profile_change_field.message(EditProfile.tennis_experience)
async def edit_tennis_experience(message: Message, state: FSMContext):
    field_name = 'tennis_experience'

    if message.text:
        string = await title.filter_symbols(str(message.text), 255, 'any')

        if string is not False and len(string) > 2:
            await state.update_data(tennis_experience=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', message.text)
            await message.answer(message_out)
            await state.set_state(EditProfile.tennis_experience)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.tennis_experience)


@router_profile_change_field.message(EditProfile.description)
async def edit_description(message: Message, state: FSMContext):
    field_name = 'description'

    if message.text:
        string = await title.filter_symbols(str(message.text), 255, 'any')

        if string is not False and len(string) > 2:
            await state.update_data(description=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out)
            await profile_main.command_profile_handler(message)
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', message.text)
            await message.answer(message_out)
            await state.set_state(EditProfile.description)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.description)


@router_profile_change_field.message(EditProfile.phone_number)
async def edit_phone_number(message: Message, state: FSMContext):
    field_name = 'phone_number'

    if message.contact:
        # contact_info = message.contact
        phone_number = message.contact.phone_number
        await state.update_data(phone_number=phone_number)
        # data = await state.get_data()
        message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', phone_number)
        user_manager = User(message.chat.id)
        params = {field_name: str(phone_number)}
        await user_manager.update(params)
        await message.answer(message_out, reply_markup=ReplyKeyboardRemove())
        await profile_main.command_profile_handler(message)
        await state.clear()
    elif message.text:
        # regular expression
        reg = '^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$'
        string = await title.filter_symbols(str(message.text), 12, 'any', reg)

        if string is not False and len(string) > 0:
            await state.update_data(phone_number=string)
            # data = await state.get_data()
            message_out = await title.load_title(message.chat.id, f'profile_new_{field_name}', string)
            user_manager = User(message.chat.id)
            params = {field_name: str(string)}
            await user_manager.update(params)
            await message.answer(message_out, reply_markup=ReplyKeyboardRemove())
            await profile_main.command_profile_handler(message)
            # ReplyKeyboardRemove()
            await state.clear()
        else:
            message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', message.text)
            await message.answer(message_out)
            await state.set_state(EditProfile.phone_number)
    else:
        message_out = await title.load_title(message.chat.id, f'profile_error_{field_name}', await title.load_title(message.chat.id, 'system_error_not_text'))
        await message.answer(message_out)
        await state.set_state(EditProfile.phone_number)


@router_profile_change_field.message(EditProfile.gender)
async def edit_gender(message: Message, state: FSMContext):
    field_name = 'gender'

    if message.text:
        print(f'skip')
    else:
        print(f'skip')


@router_profile_change_field.callback_query(lambda c: re.match(r'gender', c.data))
async def reg_ntrp(callback: CallbackQuery, state: FSMContext):
    split = callback.data.split('-')
    prefix, arg = split
    field_name = 'gender'

    await callback.answer(f'{prefix} {arg}')

    if arg == 'male':
        user_manager = User(callback.message.chat.id)
        params = {'gender': str(arg)}
        await user_manager.update(params)
        await callback.message.edit_text(await title.load_title(callback.message.chat.id, f'profile_new_{field_name}'))
        await profile_main.command_profile_handler(callback.message)
        await state.clear()
        print('male')
        # await callback.message.edit_text(message_out, reply_markup=None)
        # await state.set_state(Registration.ntrp)
    elif arg == 'female':
        user_manager = User(callback.message.chat.id)
        params = {'gender': str(arg)}
        await user_manager.update(params)
        await callback.message.edit_text(await title.load_title(callback.message.chat.id, f'profile_new_{field_name}'))
        await profile_main.command_profile_handler(callback.message)
        await state.clear()
        print('female')
        # await callback.message.edit_text(message_out,reply_markup=await markup_registration.inline_ntrp_accept(callback.message.chat.id))
