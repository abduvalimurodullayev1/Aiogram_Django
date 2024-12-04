from aiogram import Router, types, F
from aiogram.filters import Command
from apps.bot.keyboards.inline import inline_main_menu

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Quyidagilardan birini tanlang", reply_markup=inline_main_menu())


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer("Available commands:\n/start - Start the bot\n/help - Get help")
