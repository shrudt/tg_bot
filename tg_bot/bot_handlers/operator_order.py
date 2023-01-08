import re
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage


from tg_bot.config_reader import config
from tg_bot.bot_keyboards.keyboards import *
from tg_bot.bot_messages.messages import *
from tg_bot.bot_states.states import States
from tg_bot.db.db_controller import db_insert_phone
from tg_bot.bot_statistic.statistic import send_statistic


operator_logger = logging.getLogger('op_logger')
operator_router = Router()


@operator_router.message(States.PHONE_STATE, F.content_type.in_('text'))
async def phone_answer(message: types.Message, state: FSMContext):
    if re.match(r'[0-9]{11}', message.text) and len(message.text) == 11:
        await state.update_data(phone_number=message.text)
        await state.set_state(States.GEO_STATE)
        await message.answer(dialog_messages['geo_request'], reply_markup=geo_keyboard())
    else:
        await state.set_state(States.PHONE_STATE)
        await message.answer(error_messages['error_number'])


@operator_router.message(States.GEO_STATE, F.content_type.in_('location'))
async def geo_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db_insert_phone(data['user_id'], data['phone_number'])
    coord = f'Номер пользовтеля {data["phone_number"]}, {message.location.latitude}, {message.location.longitude}'
    await SendMessage(chat_id=config.chat_id.get_secret_value(), text=coord)
    await SendMessage(chat_id=data['user_id'], text=dialog_messages['wait_operator'], reply_markup=main_keyboard())
    await state.clear()
    await state.set_state(States.MENU_STATE)


@operator_router.message(States.GEO_STATE, F.text == "Продолжить без местоположения")
async def no_geo_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db_insert_phone(data["user_id"], data['phone_number'])
    await message.answer(dialog_messages['wait_operator'], reply_markup=main_keyboard())
    await SendMessage(chat_id=config.chat_id.get_secret_value(), text=f'Номер пользовтеля {data["phone_number"]}')
    send_statistic('order', user_id=data["user_id"])
    await state.clear()
    await state.set_state(States.MENU_STATE)


@operator_router.message(States.PHONE_STATE)
async def phone_state_error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await SendMessage(chat_id=data['user_id'], text=error_messages['error_number'])


@operator_router.message(States.GEO_STATE)
async def geo_state_error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await SendMessage(chat_id=data['user_id'], text=error_messages['error_geo'], reply_markup=geo_keyboard())




