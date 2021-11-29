import datetime
from celery import shared_task

from telega.client import bot
from squad.services import get_today_birthday_players


@shared_task
def notify_birthdays():
    for player in get_today_birthday_players():
        text = f"\
        Від імені команди вітаємо {player.full_name} з днем народження! 🥳🥳🥳🥳🥳⚽️🔨\n\
        {player.first_name} святкує {player.years}-річчя!"
        photo_urls = [f'https://tempfc.club{player.photo.url}']
        bot.send_album(photo_urls=photo_urls, caption=text)
