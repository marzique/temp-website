from datetime import datetime
from typing import Iterable

from squad.models import Player


def get_today_birthday_players() -> Iterable[Player]:
    qs = Player.objects.filter(
        date_of_birth__month=datetime.now().month,
        date_of_birth__day=datetime.now().day
    )
    return qs
