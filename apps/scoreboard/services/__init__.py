from scoreboard.services.hfl import HFLScoreboardService
from scoreboard.models import League, TeamInfo


def get_latest_league_context():
    leagues = League.objects.order_by('id').filter(active=True)
    if leagues.exists():
        league_id = leagues.first().id
        league = League.objects.get(id=league_id)
        teams = league.teams.select_related('team')
        return teams.order_by('place')


def update_teams_medals():
    """Add medals for teams in scoreboard if mathematically guaranteed."""
    teams_data = get_latest_league_context()
    if teams_data:
        league = teams_data.first().league
        matches_per_season = (teams_data.filter(abandoned=False).count() - 1) * league.rounds
        for teaminfo in teams_data:
            if teaminfo.place in [1, 2, 3]:
                max_points = (matches_per_season - teaminfo.games) * 3
                prev_team_games = TeamInfo.objects.get(
                    league=league,
                    place=teaminfo.place + 1
                ).games
                prev_team_max_points = (matches_per_season - prev_team_games) * 3
                if prev_team_max_points < max_points or prev_team_games == matches_per_season:
                    teaminfo.medal = teaminfo.place
            else:
                teaminfo.medal = None
            teaminfo.save()


__all__ = ['HFLScoreboardService', ]
