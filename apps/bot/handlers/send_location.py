from asgiref.sync import sync_to_async
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from apps.bot.handlers.start_order import start_order
from apps.bot.keyboards.inline import inline_categories, inline_nearest_branches
from apps.bot.utils.db_manager import db
from apps.bot.utils.functions import get_address, haversine
from apps.bot.utils.states import OrderStateGroup
from apps.bot.keyboards.reply import reply_main_menu
import logging
from apps.bot.models import *

router = Router()


@sync_to_async
def create_order(telegram_id, order_type, branch_id, longitude, latitude):

    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        raise ValueError("Foydalanuvchi topilmadi!")

    branch = Branch.objects.filter(id=branch_id).first()
    if not branch:
        raise ValueError("Filial topilmadi!")

    price = 100

    order = Order.objects.create(
        user=user,
        order_type=order_type,
        branch=branch,
        delivery_longitude=longitude,
        delivery_latitude=latitude,
        status="pending",
        price=price
    )

    return order


@sync_to_async
def get_all_branches():
    """Filiallarni ORM orqali olish"""
    return list(
        Branch.objects.values(
            'id',
            'name',
            'latitude',
            'longitude',
            'max_delivery_distance'
        )
    )


@sync_to_async
def all_categories():
    return list(
        Category.objects.values(
            'name',
            'description',
            'price',
            'image'
        )
    )


@router.message(F.text == "Orqaga", OrderStateGroup.send_location)
async def order_message(message: types.Message, state: FSMContext):
    await start_order(update=message, state=state)


@router.message(F.location, OrderStateGroup.send_location)
async def order_book_message(message: types.Message, state: FSMContext, user: User):
    if not message.location:
        await message.answer("Iltimos, joylashuvni yuboring!")
        return

    user_longitude, user_latitude = message.location.longitude, message.location.latitude

    branches = await get_all_branches()

    if not branches:
        return await message.answer("Hozirda restoranlar mavjud emas.")

    for branch in branches:
        branch['distance'] = await haversine(user_longitude, user_latitude, branch['longitude'], branch['latitude'])

    branches.sort(key=lambda branch: branch['distance'])

    address_line = await get_address(longitude=user_longitude, latitude=user_latitude)
    await message.answer(f"Sizning joylashuviz: {address_line}")

    order_data = await state.get_data()
    order_type = order_data.get('order_type', None)

    if order_type == 'delivery':
        if branches[0]['distance'] > branches[0]['max_delivery_distance']:
            return await message.answer('Выбранная локация находится вне зоны доставки.')

        await state.update_data({'branch_id': branches[0]['id']})

        categories = await all_categories()
        await message.answer("Lokatsiya qabul qilindi", reply_markup=reply_main_menu())
        await message.answer("Buyurtmani birga joylashtiramizmi? 🤗"
                             "\nKategoriyalardan birini tanlang", reply_markup=await inline_categories())
        await state.set_state(OrderStateGroup.choose_food)
        await create_order(
            user.telegram_id,
            order_type,
            branches[0]['id'],
            message.location.longitude,
            message.location.latitude
        )

    elif order_type == 'take_away':
        await message.answer("Eng yaqin restoranlar", reply_markup=inline_nearest_branches(branches))
        await state.set_state(OrderStateGroup.choose_branch_for_take_away)
