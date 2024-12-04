from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.keyboards.inline import inline_main_menu
from apps.bot.keyboards.reply import reply_start_order, reply_send_location
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction
from apps.bot.utils.states import OrderStateGroup
from apps.bot.models import Category, Product  # Importing models
from asgiref.sync import sync_to_async

router = Router()


@sync_to_async
def get_categories():
    return list(Category.objects.all().values('id', 'name', 'description', 'price'))


@sync_to_async
def get_products_by_category(category_id):
    return list(Product.objects.filter(category_id=category_id).values('id', 'name', 'price'))


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.ORDER))
async def start_order(update: [types.CallbackQuery, types.Message], state: FSMContext):
    if isinstance(update, types.CallbackQuery):
        callback_query = update
        categories = await get_categories()

        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for category in categories:
            button = InlineKeyboardButton(
                text=f"{category['name']} - {category['price']} UZS",
                callback_data=f"category_{category['id']}"
            )
            keyboard.inline_keyboard.append([button])

        await callback_query.message.answer(
            f"Buyurtmani birga joylashtiramizmi? 🤗 Buyurtma turini tanlang?",
            reply_markup=keyboard
        )

    if isinstance(update, types.Message):
        message = update
        categories = await get_categories()  # Get categories from DB

        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for category in categories:
            button = InlineKeyboardButton(
                text=f"{category['name']} - {category['price']} UZS",
                callback_data=f"category_{category['id']}"
            )
            keyboard.inline_keyboard.append([button])  # Add buttons inside a list to form rows

        await message.answer(
            "Buyurtmani birga joylashtiramizmi? 🤗 Buyurtma turini tanlang?",
            reply_markup=keyboard
        )

    await state.set_state(OrderStateGroup.order_type)


# Handler to display products based on category selection
@router.callback_query(lambda c: c.data.startswith('category_'))
async def category_selected(callback_query: types.CallbackQuery, state: FSMContext):
    category_id = int(callback_query.data.split('_')[1])  # Get category ID
    products = await get_products_by_category(category_id)  # Get products by category ID

    if products:
        message_text = "Ushbu kategoriyada quyidagi mahsulotlar mavjud:\n"
        for product in products:
            message_text += f"{product['name']} - {product['price']} UZS\n"
    else:
        message_text = "Ushbu kategoriyada mahsulotlar mavjud emas."

    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(message_text)  # Update message with products


@router.message(F.text == "Orqaga")
async def order_message(message: types.Message, state: FSMContext):
    await message.answer("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove())
    await message.answer("Quyidagilardan birini tanlang", reply_markup=inline_main_menu())
    await state.clear()


@router.message(F.text == 'Borib olish', OrderStateGroup.order_type)
async def order_book_message(message: types.Message, state: FSMContext):
    await message.answer("Borib olish uchun geo-joylashuvni jo'nating, sizga yaqin bo'lgan filialni aniqlaymiz",
                         reply_markup=reply_send_location())
    await state.update_data({'order_type': 'take_away'})
    await state.set_state(OrderStateGroup.send_location)


@router.message(F.text == 'Eltib berish', OrderStateGroup.order_type)
async def order_delivery_message(message: types.Message, state: FSMContext):
    await message.answer("Eltib berish uchun geo - joylashuvni jo'nating yoki manzilni tanlang",
                         reply_markup=reply_send_location())
    await state.update_data({'order_type': 'delivery'})
    await state.set_state(OrderStateGroup.send_location)
