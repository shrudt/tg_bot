from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.partner_api.ct_api import web_app


def main_keyboard():
    calculate_operator = KeyboardButton(text='Заказать звонок')
    calculate_self = KeyboardButton(text="Рассчитать самостоятельно", web_app=web_app)
    manual = KeyboardButton(text='Памятка перед эвакуацией')
    return ReplyKeyboardBuilder().add(calculate_operator, calculate_self, manual).adjust(1, repeat=True).as_markup(resize_keyboard=True)


def geo_keyboard():
    send_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    without_geo = KeyboardButton(text='Продолжить без местоположения')
    return ReplyKeyboardBuilder().add(send_geo, without_geo).adjust(1).as_markup(resize_keyboard=True)


def admin_keyboard():
    unblock_user = KeyboardButton(text="Разблокировать пользователя")
    return ReplyKeyboardBuilder().add(unblock_user).adjust(1).as_markup(resize_keyboard=True)