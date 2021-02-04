import datetime
from celery import shared_task

from telega.client import TelegramBot
from squad.utils import get_todays_birthday_players


bot = TelegramBot()


@shared_task
def notify_birthdays():
    for player in get_todays_birthday_players():
        text = f"\
        Від імені команди вітаємо {player.full_name} з днем народження! 🥳🥳🥳🥳🥳⚽️🔨\n\
        {player.first_name} святкує {player.years}-річчя!"
        photo_urls = [f'https://tempfc.club{player.photo.url}']
        bot.send_album(photo_urls=photo_urls, caption=text)


@shared_task
def test_timezone_messages():
    bot.send_text('TEST 18:00 Kyiv Time', chat_id=bot.TECH_CHANNEL_ID)
