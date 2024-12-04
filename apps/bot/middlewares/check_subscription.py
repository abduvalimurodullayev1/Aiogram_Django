from apps.bot.config import config
from typing import Callable, Dict, Any, Awaitable
from loguru import logger
from aiogram.types import Update, User, ChatMember
from aiogram import BaseMiddleware, Bot

from apps.bot.keyboards.inline import inline_subscribe

EVENT_FROM_USER = 'event_from_user'


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user: User = data.get(EVENT_FROM_USER)

        try:
            chat_member: ChatMember = await bot.get_chat_member(chat_id=config.SUBSCRIPTION_CHANNEL_ID, user_id=user.id)
            if chat_member.status not in ("member", "administrator", "creator"):
                return await bot.send_message(chat_id=user.id, text='Subscribe to the group',
                                              reply_markup=inline_subscribe())
        except Exception as e:
            logger.error(f"Failed to check subscription: {e}")
            return await bot.send_message(chat_id=user.id,
                                          text="Could not verify subscription status, please try again later.")

        return await handler(event, data)


__all__ = [
    'CheckSubscriptionMiddleware'
]
