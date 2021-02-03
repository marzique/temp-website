import datetime
from celery import shared_task

from telega.client import TelegramBot
from squad.utils import get_todays_birthday_players


bot = TelegramBot()


@shared_task
def notify_birthdays():
    for player in get_todays_birthday_players():
        text = f"""
        Від імені команди вітаємо {player.full_name} з днем народження!
        {player.first_name} святкує {player.years}річчя!
        https://tempfc.club{player.photo.url}
        """
        bot.send_text(text)

