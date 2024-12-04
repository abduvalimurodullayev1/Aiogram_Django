from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.bot.utils.db_manager import db
from apps.bot.utils.callback_data import cb_main_menu_callback_data, MainMenuAction, cb_back_to_main_menu_callback_data, \
    cb_select_language_callback_data, SelectLanguage, BranchCallbackData, \
    CategoryCallbackData, back_to_food_menu_callback_data, \
    BackToFoodMenuAction, ProductItemOrderCallbackData, ProductOrderCallbackData, cb_update_city_callback_data, \
    UpdateCity, MyOrdersCallbackData, cb_select_settings_callback_data, SelectSettingsAction
from aiogram import types
from asgiref.sync import sync_to_async
from apps.bot.models import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_back_to_main_menu():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='Asosiy menu',
                           callback_data=cb_back_to_main_menu_callback_data())
    return inline_keyboard.as_markup()


def inline_main_menu():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='🏠️️ Buyurtma berish',
                           callback_data=cb_main_menu_callback_data(action=MainMenuAction.ORDER))
    inline_keyboard.button(text='Biz haqimizda', callback_data=cb_main_menu_callback_data(action=MainMenuAction.ABOUT))
    inline_keyboard.button(text='Buyurtmalarim',
                           callback_data=cb_main_menu_callback_data(action=MainMenuAction.MY_ORDERS))
    inline_keyboard.button(text='Filiallar', callback_data=cb_main_menu_callback_data(action=MainMenuAction.BRANCHES))
    inline_keyboard.button(text='Sozlamalar', callback_data=cb_main_menu_callback_data(action=MainMenuAction.SETTINGS))

    inline_keyboard.adjust(2)

    return inline_keyboard.as_markup()


def inline_subscribe():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='Subscribe', url='https://t.me/oqtepalavashuz')

    return inline_keyboard.as_markup()


def inline_languages():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text='Uzbek', callback_data=cb_select_language_callback_data(lang=SelectLanguage.UZ))
    inline_keyboard.button(text='Russian', callback_data=cb_select_language_callback_data(lang=SelectLanguage.RU))
    inline_keyboard.button(text='English', callback_data=cb_select_language_callback_data(lang=SelectLanguage.EN))

    inline_keyboard.adjust(1)

    return inline_keyboard.as_markup()


async def inline_branches():
    inline_keyboard = InlineKeyboardBuilder()
    branches = await db.fetch("SELECT id, name FROM branches")
    for branch in branches:
        inline_keyboard.button(
            text=branch['name'],
            callback_data=BranchCallbackData(branch_id=branch['id']).pack()
        )
    inline_keyboard.button(text='Asosiy menu',
                           callback_data=cb_back_to_main_menu_callback_data())
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


async def inline_my_orders(user_id):
    inline_keyboard = InlineKeyboardBuilder()
    my_orders = await db.get_my_orders(user_id)
    for my_order in my_orders:
        if my_order['status'] != 'created':
            text = (
                f"order_type: {my_order['order_type']}\n"
                f"branch_id: {my_order['branch_id']}\n"
                f"status: {my_order['status']}\n"
                f"total_price: {my_order['total_price']}\n"
                f"created_at: {my_order['created_at']}\n"
                f"updated_at: {my_order['updated_at']}\n"
            )
            inline_keyboard.button(
                text=text,
                callback_data=MyOrdersCallbackData(user_id=user_id).pack()
            )
    inline_keyboard.button(text='Asosiy menu',
                           callback_data=cb_back_to_main_menu_callback_data())
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


@sync_to_async
def get_categories():
    return list(Category.objects.all().values('id', 'name', 'description', 'price'))


async def inline_categories():
    categories = await get_categories()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category in categories:
        button = InlineKeyboardButton(
            text=f"{category['name']} - {category['price']} UZS",
            callback_data=CategoryCallbackData(category_id=category['id']).pack()
        )
        keyboard.inline_keyboard.append([button])

    return keyboard


async def inline_product_catalog(products: list):
    inline_keyboard = InlineKeyboardBuilder()
    for product in products:
        inline_keyboard.button(
            text=product['name'],
            callback_data=ProductOrderCallbackData(product_id=product['id']).pack()
        )
    inline_keyboard.button(text="Ortga",
                           callback_data=back_to_food_menu_callback_data(action=BackToFoodMenuAction.BACK))

    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


def inline_settings():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(
        text="Muloqot tili",
        callback_data="ignore"
    )
    inline_keyboard.button(text="Telefon",
                           callback_data=cb_select_settings_callback_data(action=SelectSettingsAction.TELEFON))
    inline_keyboard.button(text="Shahar",
                           callback_data=cb_select_settings_callback_data(action=SelectSettingsAction.SHAHAR))
    inline_keyboard.button(text="Asosiy menu", callback_data=cb_back_to_main_menu_callback_data())
    inline_keyboard.adjust(3)

    return inline_keyboard.as_markup()


async def inline_order_food_item_keyboard(product_id: int, quantity: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data=ProductItemOrderCallbackData(action="decrease",
                                                                                          product_id=product_id,
                                                                                          quantity=quantity).pack()),
                InlineKeyboardButton(text=f"{quantity}", callback_data="ignore"),
                InlineKeyboardButton(text="+", callback_data=ProductItemOrderCallbackData(action="increase",
                                                                                          product_id=product_id,
                                                                                          quantity=quantity).pack()),
            ],
            [
                InlineKeyboardButton(text="🛒 Add to Cart",
                                     callback_data=ProductItemOrderCallbackData(action="add_to_cart",
                                                                                product_id=product_id,
                                                                                quantity=quantity).pack())
            ],
            [
                InlineKeyboardButton(text="🔙 Back",
                                     callback_data=ProductItemOrderCallbackData(action="back", product_id=product_id,
                                                                                quantity=quantity).pack())
            ],
        ]
    )


def inline_nearest_branches(branches):
    inline_keyboard = InlineKeyboardBuilder()
    for branch in branches:
        inline_keyboard.button(
            text=branch['name'],
            callback_data=BranchCallbackData(branch_id=branch['id']).pack()
        )
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()


def inline_cities():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='Toshkent', callback_data=cb_update_city_callback_data(city=UpdateCity.TOSH))
    inline_keyboard.button(text='Samarqand', callback_data=cb_update_city_callback_data(city=UpdateCity.SAM))
    inline_keyboard.button(text='Andijon', callback_data=cb_update_city_callback_data(city=UpdateCity.AND))

    inline_keyboard.adjust(1)

    return inline_keyboard.as_markup()
