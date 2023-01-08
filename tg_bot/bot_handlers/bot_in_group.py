import logging


from aiogram import F, Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated
from tg_bot.config_reader import config


logger = logging.getLogger("group")
group_router = Router()
group_router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@group_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    chat_id = event.chat.id
    if str(chat_id) != config.chat_id.get_secret_value():
        await bot.leave_chat(chat_id=chat_id)
    else:
        logger.info('tg_bot added to group')
