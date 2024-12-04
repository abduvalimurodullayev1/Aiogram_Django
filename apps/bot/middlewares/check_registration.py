from aiogram.types import Update, ReplyKeyboardRemove
from aiogram import BaseMiddleware, Bot
from typing import Callable, Dict, Any, Awaitable

from apps.bot.keyboards.inline import inline_languages
from apps.bot.utils.states import OrderStateGroup, RegistrationStateGroup
from apps.bot.models import User  # Django model

EVENT_FROM_USER = 'event_from_user'


class CheckRegistrationMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        state = data['state']

        # Event ichidan `chat_id` va `telegram_id`ni olish
        telegram_id = (
            event.message.from_user.id if event.message else
            event.callback_query.from_user.id if event.callback_query else None
        )
        chat_id = (
            event.message.chat.id if event.message else
            event.callback_query.message.chat.id if event.callback_query else None
        )

        # Agar `telegram_id` yoki `chat_id` mavjud bo'lmasa, xato xabar yuborish
        if not telegram_id or not chat_id:
            return await bot.send_message(
                chat_id=chat_id,
                text="Foydalanuvchi ma’lumoti topilmadi."
            )

        # Django modelidan foydalanuvchini olish
        try:
            user_data = await User.objects.filter(telegram_id=telegram_id).afirst()
        except Exception as e:
            return await bot.send_message(
                chat_id=chat_id,
                text=f"Xatolik yuz berdi: {str(e)}"
            )

        # Foydalanuvchini ro‘yxatdan o‘tkazilganligini tekshirish
        current_state = await state.get_state()
        if not user_data and current_state in OrderStateGroup.__all_states__:
            await bot.send_message(
                chat_id=chat_id,
                text='Iltimos, avval registratsiyadan o‘ting.',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(RegistrationStateGroup.language)
            return await bot.send_message(
                chat_id=chat_id,
                text='Tilni tanlang.',
                reply_markup=inline_languages()
            )

        # Foydalanuvchini `data`ga qo‘shish
        data['user'] = user_data

        return await handler(event, data)


__all__ = [
    'CheckRegistrationMiddleware'
]
