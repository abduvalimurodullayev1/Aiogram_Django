from .commands import router as commands_router
from .about import router as about_router
from .send_location import router as send_location
from .start_order import router as start_order
from .registration import router as registration
from .branches import router as branches
from .choose_food import router as choose_food
from .settings import router as settings
from .select_branch import router as select_branch
from .my_orders import router as my_orders


def setup_handlers(dp):
    dp.include_router(commands_router)
    dp.include_router(send_location)

    # dp.include_router(settings)

    dp.include_router(select_branch)

    dp.include_router(branches)

    dp.include_router(my_orders)

    dp.include_router(choose_food)

    dp.include_router(start_order)

    dp.include_router(about_router)

    dp.include_router(registration)
