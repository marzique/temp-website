from django.conf import settings
from django.urls import path
from telega.views import TelegramWebhookView


urlpatterns = [
    path(f'{settings.TELEGRAM_BOT_TOKEN}/', TelegramWebhookView.as_view(), name='telegram-webhook'),
]
