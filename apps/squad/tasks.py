import datetime
from celery import shared_task

from telega.client import TelegramBot


bot = TelegramBot()


@shared_task
def notify_birthdays():
    bot.send_text(f'ТЕСТ ТЕСТ ТЕСТ 5 минут')

