import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from apps.bot.handlers import setup_handlers
from apps.bot.middlewares import setup_middlewares
from apps.bot.config import config

redis = Redis.from_url(config.REDIS_URL)
dp = Dispatcher(storage=RedisStorage(redis=redis))

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

setup_middlewares(dp)
setup_handlers(dp)

# Event loop yaratish
loop = asyncio.get_event_loop()
