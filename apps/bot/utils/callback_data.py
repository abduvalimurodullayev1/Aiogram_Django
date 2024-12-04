from enum import Enum
from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel

# Main Menu Actions
class MainMenuAction(str, Enum):
    ORDER = 'order'
    ABOUT = 'about'
    MY_ORDERS = 'my_orders'
    BRANCHES = 'branches'
    SETTINGS = 'settings'


class MainMenuCallbackData(CallbackData, prefix='main_menu'):
    action: MainMenuAction


def cb_main_menu_callback_data(action: MainMenuAction):
    return MainMenuCallbackData(action=action).pack()


# Back to Main Menu Actions
class BackToMainMenuAction(str, Enum):
    BACK = 'back'


class BackToMainMenuCallbackData(CallbackData, prefix='back_main_menu'):
    action: BackToMainMenuAction


def cb_back_to_main_menu_callback_data():
    return BackToMainMenuCallbackData(action=BackToMainMenuAction.BACK).pack()


# Language Selection Actions
class SelectLanguage(str, Enum):
    UZ = 'uz'
    RU = 'ru'
    EN = 'en'


class SelectLanguageCallbackData(CallbackData, prefix='select_language'):
    language: SelectLanguage


def cb_select_language_callback_data(lang: SelectLanguage):
    return SelectLanguageCallbackData(language=lang).pack()


# Branch Selection
class BranchCallbackData(CallbackData, prefix="branch"):
    branch_id: int


# My Orders Selection
class MyOrdersCallbackData(CallbackData, prefix="my_order"):
    user_id: int


# Back to Food Menu Actions
class BackToFoodMenuAction(str, Enum):
    BACK = 'back'


class BackToFoodMenuCallbackData(CallbackData, prefix='food_menu'):
    action: BackToFoodMenuAction


def cb_back_to_food_menu_callback_data(action: BackToFoodMenuAction):
    return BackToFoodMenuCallbackData(action=action).pack()


# Category Selection
class CategoryCallbackData(CallbackData, prefix="category"):
    category_id: int


# Product Order Callback Data
class ProductOrderCallbackData(CallbackData, prefix="product"):
    product_id: int


# Product Item Order Callback Data
class ProductItemOrderCallbackData(CallbackData, prefix="product_order"):
    action: str
    product_id: int
    quantity: int


# Settings Actions
class SelectSettingsAction(str, Enum):
    MULOQOT_TILI = 'muloqot_tili'
    TELEFON = 'telefon'
    SHAHAR = 'shahar'


class SelectSettingsCallbackData(CallbackData, prefix='settings'):
    action: SelectSettingsAction


def cb_select_settings_callback_data(action: SelectSettingsAction):
    return SelectSettingsCallbackData(action=action).pack()


# City Update Actions
class UpdateCity(str, Enum):
    TOSH = 'Toshkent'
    SAM = 'Samarkand'
    AND = 'Andijon'


class UpdateCityCallbackData(CallbackData, prefix='select_city'):
    city: UpdateCity


def cb_update_city_callback_data(city: UpdateCity):
    return UpdateCityCallbackData(city=city).pack()


def back_to_food_menu_callback_data(action: BackToFoodMenuAction):
    return BackToFoodMenuCallbackData(action=action).pack()
