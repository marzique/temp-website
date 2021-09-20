from scoreboard.models import League


def get_latest_league_context():
    leagues = League.objects.order_by('id').filter(active=True)
    if leagues.exists():
        return leagues.first().teams.select_related('team').order_by('place')
