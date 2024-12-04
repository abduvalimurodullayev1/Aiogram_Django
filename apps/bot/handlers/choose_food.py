from apps.bot.keyboards.inline import inline_categories, inline_product_catalog, \
    inline_order_food_item_keyboard
from apps.bot.utils.callback_data import CategoryCallbackData, \
    BackToFoodMenuCallbackData, BackToFoodMenuAction, ProductOrderCallbackData
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from apps.bot.utils.callback_data import ProductItemOrderCallbackData
from apps.bot.utils.db_manager import db

router = Router()


# @router.message(F.text == "Ortga", OrderStateGroup.choose_food)
# async def back_from_choose_branch(message: types.Message, state: FSMContext):
#     await message.answer("Buyurtma turini tanlang", reply_markup=reply_start_order())
#
# @router.message(F.text, OrderStateGroup.choose_food)
# async def food_menu_for_take_away(message: types.Message, state: FSMContext):
#     await state.set_state(OrderStateGroup.choose_food)
#
#     await message.answer("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove())
#     await message.answer("Kategoriyalardan birini tanlang.", parse_mode="HTML", reply_markup=await inline_categories())


@router.callback_query(BackToFoodMenuCallbackData.filter(F.action == BackToFoodMenuAction.BACK))
async def back_from_choose_food(callback_query: types.CallbackQuery, state: FSMContext):
    categories = await db.get_categories()
    await callback_query.message.answer("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove())
    await callback_query.message.answer("Kategoriyalardan birini tanlang.",
                                        reply_markup=await inline_categories())


@router.callback_query(CategoryCallbackData.filter())
async def choose_food_message(callback_query: types.CallbackQuery, callback_data: CategoryCallbackData,
                              state: FSMContext):
    category = await db.get_category(callback_data.category_id)
    products = await db.get_products(callback_data.category_id)

    photo = FSInputFile(category['image'])

    await callback_query.message.answer_photo(
        photo,
        caption=f"category: {category['name']}",
        parse_mode="Markdown",
        reply_markup=await inline_product_catalog(products)
    )


@router.callback_query(ProductOrderCallbackData.filter())
async def order_food_item_message(callback_query: types.CallbackQuery, callback_data: ProductOrderCallbackData):
    product = await db.get_product(callback_data.product_id)

    photo = FSInputFile(product['image'])

    initial_quantity = 1

    await callback_query.message.answer_photo(
        photo,
        caption=f"product: {product['name']}",
        parse_mode="Markdown",
        reply_markup=await inline_order_food_item_keyboard(product['id'], initial_quantity)
    )


@router.callback_query(ProductItemOrderCallbackData.filter())
async def handle_product_order(callback_query: types.CallbackQuery, callback_data: ProductItemOrderCallbackData, user):
    action = callback_data.action
    product_id = callback_data.product_id
    quantity = callback_data.quantity
    product = await db.get_product(product_id)
    price = product['price']
    if action == "increase":
        quantity += 1
    elif action == "decrease" and quantity > 1:
        quantity -= 1
    elif action == "add_to_cart":
        order = await db.get_current_order(user['telegram_id'])
        await db.create_or_update_order_item(order['id'], product_id, quantity)
        await callback_query.message.answer("✅ Added to cart!")
        return
    elif action == "back":
        await callback_query.message.delete()
        return

    await callback_query.message.edit_reply_markup(
        reply_markup=await inline_order_food_item_keyboard(product['id'], quantity)
    )
