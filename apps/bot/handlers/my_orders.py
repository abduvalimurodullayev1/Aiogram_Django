from aiogram import Router, types, F
from apps.bot.keyboards.inline import inline_branches, inline_my_orders
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction, BranchCallbackData
from apps.bot.utils.db_manager import db
from apps.bot.utils.states import OrderStateGroup

router = Router()


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.MY_ORDERS))
async def my_orders(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.answer("Barcha buyurtmalaringiz: ", reply_markup=await inline_my_orders(user_id))
