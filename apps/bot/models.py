from django.db import models
from solo.models import SingletonModel
from apps.common.models import *

# apps/bot/models.py
from django.db import models


class TelegramBotConfiguration(models.Model):
    bot_token = models.CharField(max_length=255, default="token")
    secret_key = models.CharField(max_length=255, default="secret_key")
    admin = models.IntegerField(default=1)
    webhook_url = models.URLField(max_length=255, default="https://7bb8-185-213-229-51.ngrok-free.app/webhook/")


class User(models.Model):
    telegram_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=122)
    username = models.CharField(max_length=122)
    language = models.CharField(max_length=122)
    phone = models.CharField(max_length=122)
    city = models.CharField(max_length=122)


class Branch(models.Model):
    name = models.CharField(max_length=122)
    address = models.CharField(max_length=122)
    city = models.CharField(max_length=122)
    open_time = models.TimeField()
    close_time = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    max_delivery_distance = models.FloatField()


class Category(models.Model):
    name = models.CharField()
    description = models.TextField(max_length=122)
    price = models.FloatField()
    size = models.CharField()
    image = models.ImageField(upload_to='image/')


class Order(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=122)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    delivery_longitude = models.FloatField()  # Eski d_longitude o'rniga
    delivery_latitude = models.FloatField()  # Eski d_latitude o'rniga
    status = models.CharField(max_length=122, default="created")
    price = models.FloatField()


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    description = models.TextField(max_length=122)
    price = models.FloatField()
    size = models.CharField(max_length=122)
    image = models.ImageField(upload_to="product/")


class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
