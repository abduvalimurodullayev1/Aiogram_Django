from django.http import JsonResponse
from django.views import View
from aiogram import Bot, Dispatcher, types
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from apps.bot.config.bot import bot, dp
import asyncio


async def skip_old_updates(bot):
    await bot.get_updates(offset=-1)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebHook(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            update = types.Update(**data)
            print(f"Update received: {update}")

            loop = asyncio.get_event_loop()
            await dp.feed_update(bot=bot, update=update)
            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
