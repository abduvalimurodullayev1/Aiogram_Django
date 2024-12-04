from aiogram import Router, types, F

from apps.bot.handlers.commands import start_command
from apps.bot.keyboards.inline import inline_back_to_main_menu
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction, BackToMainMenuCallbackData, \
    BackToMainMenuAction

router = Router()


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.ABOUT))
async def about_message(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        f"Buyurtmani birga joylashtiramizmi? 🤗\nBiz O‘zbekiston bozorida 12 yildan beri faoliyat yuritamiz "
        f"va bugungi kunda butun mamlakat bo‘ylab 50 dan ortiq filiallarimiz mavjud."
        f" <a href='https://t.me/oqtepalavashuz'>Telegram</a> | "
        f"<a href='https://www.youtube.com/@oqtepalavashuz'>Youtube</a>",
        reply_markup=inline_back_to_main_menu())


@router.callback_query(BackToMainMenuCallbackData.filter(F.action == BackToMainMenuAction.BACK))
async def back_to_main_menu_message(callback_query: types.CallbackQuery, callback_data: BackToMainMenuCallbackData):
    await start_command(callback_query.message)
