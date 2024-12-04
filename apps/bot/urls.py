# apps/bot/urls.py
from django.urls import path
from apps.bot.views import TelegramWebHook

urlpatterns = [
    path('webhook/', TelegramWebHook.as_view(), name='telegram-webhook'),
]
