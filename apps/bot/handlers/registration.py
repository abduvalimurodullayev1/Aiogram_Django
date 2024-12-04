from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from apps.bot.keyboards.reply import reply_send_phone_number
from apps.bot.utils.states import RegistrationStateGroup
from apps.bot.utils.callback_data import SelectLanguageCallbackData
from apps.bot.models import User

import asyncio
from concurrent.futures import ThreadPoolExecutor

router = Router()

# Executor yaratamiz
executor = ThreadPoolExecutor()


@router.callback_query(SelectLanguageCallbackData.filter())
async def start_order(callback_query: types.CallbackQuery, state: FSMContext,
                      callback_data: SelectLanguageCallbackData):
    await state.update_data({"language": callback_data.language})

    await callback_query.message.answer(f"Telefon raqamingizni jo`nating", reply_markup=reply_send_phone_number())
    await state.set_state(RegistrationStateGroup.phone)


@router.message(F.text, RegistrationStateGroup.phone)
async def receive_phone(message: types.Message, state: FSMContext):
    if not message.text.startswith('+998') or len(message.text) != 13:
        return await message.answer("To`g`ri formatda raqam jo`nating yoki buttondan foydalaning")

    await state.update_data({"phone_number": message.text})
    await state.set_state(RegistrationStateGroup.name)
    await message.answer("Ismingizni jo`nating", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.contact, RegistrationStateGroup.phone)
async def receive_contact(message: types.Message, state: FSMContext):
    await state.update_data({"phone_number": f"{message.contact.phone_number}"})
    await state.set_state(RegistrationStateGroup.name)
    await message.answer("Ismingizni jo`nating", reply_markup=types.ReplyKeyboardRemove())


async def create_user_async(data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: User.objects.get_or_create(
        telegram_id=data["telegram_id"],
        defaults={
            "language": data["language"],
            "phone": data["phone"],
            "name": data["name"],
            "username": data["username"],
        }
    ))


@router.message(F.text, RegistrationStateGroup.name)
async def receive_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    registration_data = await state.get_data()

    await message.answer(
        f"Sizning ismingiz: {registration_data['name']}\n"
        f"Telefon raqamingiz: {registration_data['phone_number']}\n"
        f"Tiliz: {registration_data['language']}\n\n"
        "Sizning registratsiyani yakunlashingiz uchun tugmasini bosing",
    )

    await create_user_async({
        "telegram_id": message.from_user.id,
        "language": registration_data['language'],
        "phone": registration_data['phone_number'],
        "name": registration_data['name'],
        "username": message.from_user.username
    })

    await state.clear()
