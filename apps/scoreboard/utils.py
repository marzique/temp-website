from scoreboard.models import League


def get_lates_league_context():
    return League.objects.order_by('id').filter(active=True).first().teams.all()
