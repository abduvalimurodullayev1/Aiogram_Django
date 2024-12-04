from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from apps.bot.keyboards.inline import inline_settings, inline_languages, inline_cities
from apps.bot.keyboards.reply import reply_send_phone_number
from apps.bot.utils.callback_data import (
    MainMenuCallbackData, MainMenuAction,
    SelectLanguageCallbackData, UpdateCityCallbackData,
    SelectSettingsCallbackData, SelectSettingsAction
)
from apps.bot.utils.db_manager import db
from apps.bot.utils.states import SettingsStateGroup

router = Router()


# Main Menu Settings Callback
@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.SETTINGS))
async def settings(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    user_data = await db.get_user(telegram_id=user.id)
    lang = user_data.get('language', 'uz')
    language = {"ru": "Русский", "en": "English", "uz": "O'zbek"}.get(lang, "Unknown")

    await callback_query.message.answer(
        "Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove()
    )
    await callback_query.message.answer(
        f"<b>Muloqot tili:</b> {language}\n"
        f"<b>Telefon:</b> {user_data.get('phone', 'Nomaʼlum')}\n"
        "<b>Shahar:</b> Toshkent\n",
        parse_mode="HTML",
        reply_markup=inline_settings()
    )


# Change Language Callback
@router.callback_query(SelectSettingsCallbackData.filter(F.action == SelectSettingsAction.MULOQOT_TILI))
async def change_language(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStateGroup.change_language)
    await callback_query.message.answer("Tilni tanlang", reply_markup=inline_languages())


# Select Language Callback
@router.callback_query(SelectLanguageCallbackData.filter(), SettingsStateGroup.change_language)
async def select_language(callback_query: types.CallbackQuery, callback_data: SelectLanguageCallbackData,
                          state: FSMContext):
    if not callback_data.language:
        await callback_query.message.answer("Til tanlanmadi. Iltimos, tilni tanlang.")
        return

    await db.update_user(language=callback_data.language, telegram_id=callback_query.from_user.id)
    await callback_query.message.answer("Til o'zgartirildi", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Change Phone Number Callback
@router.callback_query(SelectSettingsCallbackData.filter(F.action == SelectSettingsAction.TELEFON))
async def change_phone_number(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Telefon raqamingizni jo'nating!", reply_markup=reply_send_phone_number())


# Receive Phone Number
@router.message()
async def receive_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if not phone.startswith("+998") or len(phone) != 13:
        await message.answer("To'g'ri formatda raqam jo'nating yoki buttondan foydalaning")
        return

    await db.update_user(phone=phone, telegram_id=message.from_user.id)
    await message.answer("Telefon raqamingiz o'zgartirildi", reply_markup=ReplyKeyboardRemove())


# Change City Callback
@router.callback_query(SelectSettingsCallbackData.filter(F.action == SelectSettingsAction.SHAHAR))
async def change_city(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStateGroup.change_city)
    await callback_query.message.answer("Shaharni tanlang", reply_markup=inline_cities())


# Select City Callback
@router.callback_query(UpdateCityCallbackData.filter(), SettingsStateGroup.change_city)
async def select_city(callback_query: types.CallbackQuery, callback_data: UpdateCityCallbackData, state: FSMContext):
    await db.update_user(city=callback_data.city, telegram_id=callback_query.from_user.id)
    await callback_query.message.answer(
        f"Shahar o'zgartirildi: {callback_data.city}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
