from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.types import ReplyKeyboardRemove


from tg_bot.db.db_controller import db_insert_id
from tg_bot.bot_handlers import operator_order, admin_handlers
from tg_bot.bot_keyboards.keyboards import *
from tg_bot.bot_messages.messages import dialog_messages, error_messages
from tg_bot.bot_states.states import States
from tg_bot.bot_statistic.statistic import send_statistic

admin_list = []

router = Router()
router.include_router(operator_order.operator_router)
router.include_router(admin_handlers.admin_router)


@router.message(Command(commands=["super"]))
async def admin_menu(mess: types.Message, state: FSMContext):
    if str(mess.from_user.id) in admin_list:
        await mess.answer('Привет, Админ!', reply_markup=admin_keyboard())
        await state.set_state(States.ADMIN_STATE)
    else:
        await mess.answer(text=error_messages['error_menu'])


@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    send_statistic('start', user_id=message.from_user.id)
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    db_insert_id(str(message.from_user.id))
    await state.set_state(States.MENU_STATE)
    await message.answer(dialog_messages['welcome'], reply_markup=main_keyboard())


@router.message(States.MENU_STATE, F.content_type.in_('text'))
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == 'Заказать звонок':
        send_statistic('phone', user_id=message.from_user.id)
        await state.update_data(user_id=message.from_user.id)
        await state.set_state(States.PHONE_STATE)
        await message.answer(dialog_messages['phone_number'], reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Памятка перед эвакуацией':
        await message.answer(dialog_messages['channel'], reply_markup=main_keyboard())
    else:
        await message.answer(error_messages['error_menu'])


@router.message(States.MENU_STATE)
async def menu_state_error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await SendMessage(chat_id=data['user_id'], text=error_messages['error_menu'])


