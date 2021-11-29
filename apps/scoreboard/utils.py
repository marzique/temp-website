from scoreboard.models import League


def get_latest_league_context():
    leagues = League.objects.order_by('id').filter(active=True)
    if leagues.exists():
        return leagues.first().teams.select_related('team').order_by('place')


def update_teams_medals():
    """Add medals for teams in scoreboard if mathematically guaranteed."""
    teams_data = get_latest_league_context()
    if teams_data:
        league = teams_data.first().league
        teams_count = league.teams.count()

    for teaminfo in teams_data:
        if teaminfo.place in [1, 2, 3]:
            pass
        else:
            teaminfo.medal = None
        teaminfo.save()
