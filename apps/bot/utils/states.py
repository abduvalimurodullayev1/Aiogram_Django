from aiogram.fsm.state import StatesGroup, State


class RegistrationStateGroup(StatesGroup):
    language = State()
    phone = State()
    name = State()
    finish = State()


class OrderStateGroup(StatesGroup):
    order_type = State()
    send_location = State()
    choose_branch_for_take_away = State()
    choose_food = State()


class SettingsStateGroup(StatesGroup):
    change_language = State()
    change_phone = State()
    change_city = State()
