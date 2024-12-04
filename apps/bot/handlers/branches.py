from aiogram import Router, types, F
from apps.bot.keyboards.inline import inline_branches
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction, BranchCallbackData
from apps.bot.utils.db_manager import db
from apps.bot.utils.states import OrderStateGroup

router = Router()


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.BRANCHES))
async def branches(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Bizning filiallarimiz: ", reply_markup=await inline_branches())


@router.callback_query(BranchCallbackData.filter(), F.state != OrderStateGroup.choose_branch_for_take_away)
async def show_branch_details(callback_query: types.CallbackQuery, callback_data: BranchCallbackData):
    branch_id = callback_data.branch_id

    branch = await db.fetch_one(
        "SELECT name, open_time, close_time, address, latitude, longitude "
        "FROM branches WHERE id = $1",
        branch_id
    )

    if not branch:
        await callback_query.message.answer("Filial topilmadi.")
        return

    open_time = branch['open_time'].strftime("%H:%M")
    close_time = branch['close_time'].strftime("%H:%M")

    location_link = f"https://www.google.com/maps?q={branch['latitude']},{branch['longitude']}"

    text = (
        f"🏠  <b>{branch['name']}</b>\n"
        f"🕒 {open_time} - {close_time}\n"
        f"📍 <a href='{location_link}'>{branch['address']}</a>"
    )

    await callback_query.message.answer(text=text, parse_mode="HTML", reply_markup=await inline_branches())
