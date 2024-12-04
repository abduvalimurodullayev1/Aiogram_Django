from aiogram import Router, types, F
import logging
from apps.bot.handlers.send_location import order_book_message
from apps.bot.keyboards.inline import inline_categories
from apps.bot.utils.callback_data import BranchCallbackData
from apps.bot.utils.db_manager import db
from apps.bot.utils.states import OrderStateGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

router = Router()
from apps.bot.models import *


@router.message(F.text == "Orqaga", OrderStateGroup.choose_branch_for_take_away)
async def back_to_send_location(message: types.Message, state: FSMContext):
    # Foydalanuvchi ma'lumotini olish
    telegram_id = message.from_user.id
    user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()

    if not user:
        return await message.answer("Foydalanuvchi topilmadi!")

    await order_book_message(message=message, state=state, user=user)


@router.callback_query(BranchCallbackData.filter(), OrderStateGroup.choose_branch_for_take_away)
async def show_branch_details(callback_query: types.CallbackQuery, callback_data: BranchCallbackData, state: FSMContext,
                              user):
    logging.info(f"User\n\n\n\n\n: {user}")
    branch_id = callback_data.branch_id
    categories = await db.get_categories()
    order_data = await state.get_data()

    await state.update_data({"branch_id": branch_id})

    await callback_query.message.answer("Buyurtmani birga joylashtiramizmi? 🤗",
                                        reply_markup=types.ReplyKeyboardRemove())
    await callback_query.message.answer("Kategoriyalardan birini tanlang.",
                                        reply_markup=await inline_categories(categories))

    await state.set_state(OrderStateGroup.choose_food)

    await db.create_order(user['telegram_id'], order_data['type_order'], branch_id, None, None)
