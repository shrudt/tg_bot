from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from tg_bot.config_reader import config
from tg_bot.bot_middleware.anti_spam import spam_catcher, check_blocked


class MessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if not str(event.chat.id) == config.chat_id.get_secret_value():
            if check_blocked(event.from_user.id):
                await spam_catcher(event)
                return await handler(event, data)





