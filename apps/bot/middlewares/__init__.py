from .logging import *
from .check_subscription import *
from .check_registration import *


def setup_middlewares(dp):
    dp.update.outer_middleware(LoggingMiddleware())
    # dp.update.outer_middleware(CheckSubscriptionMiddleware())
    dp.update.outer_middleware(CheckRegistrationMiddleware())
