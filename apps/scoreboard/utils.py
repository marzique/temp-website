from scoreboard.models import League


def get_lates_league_context():
    leagues = League.objects.order_by('id').filter(active=True)
    if leagues.exists():
        return leagues.first().teams.all()
