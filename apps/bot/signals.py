from django.dispatch import receiver
from django.db.models.signals import pre_save
import requests

from apps.bot.models import TelegramBotConfiguration


@receiver(pre_save, sender=TelegramBotConfiguration)
def update_bot_webhook_url(sender, instance, **kwargs):
    if instance._state.adding and instance.bot_token and instance.webhook_url:
        telegram_webhook_url = f'https://api.telegram.org/bot{instance.bot_token}/setWebhook?url={instance.webhook_url}'
        try:
            response = requests.get(url=telegram_webhook_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            existing_object = sender.objects.get(pk=instance.pk)
            if existing_object.webhook_url != instance.webhook_url:
                telegram_webhook_url = f'https://api.telegram.org/bot{instance.bot_token}/setWebhook?url={instance.webhook_url}'
                try:
                    response = requests.get(url=telegram_webhook_url)
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print(f"HTTPError: {e}")
                except Exception as e:
                    print(f"Error: {e}")
        except sender.DoesNotExist:
            pass
