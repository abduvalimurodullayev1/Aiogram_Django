from django.contrib import admin
from apps.bot.models import *
# Register your models here.
admin.site.register(TelegramBotConfiguration)
admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Product)
admin.site.register(Category)
