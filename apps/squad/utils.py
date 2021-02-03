from datetime import datetime, timedelta

from squad.models import Player


def get_todays_birthday_players(self):
    qs = Player.objects.filter(date_of_birth__month=datetime.now().month, date_of_birth__day=datetime.now().day)
    return qs
