from aiogram.utils.keyboard import ReplyKeyboardBuilde

def reply_send_phone_number():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text="Send phone", request_contact=True)

    return reply_keyboard.as_markup()


def reply_finish_registration():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text="Yakunlash")
    reply_keyboard.button(text="Orqaga")

    return reply_keyboard.as_markup(resize_keyboard=True)


def reply_start_order():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text="Eltib berish")
    reply_keyboard.button(text="Borib olish")
    reply_keyboard.button(text="Orqaga")

    reply_keyboard.adjust(2)

    return reply_keyboard.as_markup(resize_keyboard=True)


def reply_send_location():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text="Lokatsiya jo`natish", request_location=True)
    reply_keyboard.button(text="Orqaga")

    return reply_keyboard.as_markup(resize_keyboard=True)


def reply_choose_branch(branch):
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text=f"{branch}")
    reply_keyboard.button(text="Ortga")

    return reply_keyboard.as_markup(resize_keyboard=True)


def reply_main_menu():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text="Asosiy menu")

    return reply_keyboard.as_markup(resize_keyboard=True)
