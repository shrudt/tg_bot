from aiogram.types import WebAppInfo
from tg_bot.config_reader import config

web_app = WebAppInfo(url=config.api_url.get_secret_value())



