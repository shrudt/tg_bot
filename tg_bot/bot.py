import asyncio
import logging.config
from aiogram import Bot
from aiogram import Dispatcher
from config_reader import config
from bot_handlers import base, bot_in_group
from bot_middleware import middleware


logging.basicConfig(level='INFO')
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.message.outer_middleware(middleware=middleware.MessageMiddleware())
dp.include_router(base.router)
dp.include_router(bot_in_group.group_router)


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


