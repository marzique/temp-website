import re

import requests
from bs4 import BeautifulSoup

from django.conf import settings

from scoreboard.models import League, Team, TeamInfo


class HFLScoreboardService:
    @staticmethod
    def _get_html():
        resp = requests.get(settings.HFL_SCOREBOARD_URL)
        return resp.text

    def _extract_table(self):
        """Extract all rows with team stats from table"""

        html = self._get_html()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('div', id=re.compile('tournaments-tables-table-'))
        # use first table with temp in it
        for table in tables:
            if 'темп' in table.get_text().lower():
                rows = table.find_all(class_='table__row')
                return rows

    def get_scoreboard(self):
        rows = self._extract_table()
        if not rows:  # Couldn't parse table from services website
            return []

        teams = []
        for row in rows:
            place = row.find(class_='table__cell--number').get_text().strip()
            logo_url = row.find(class_='table__team-img').get('src')
            name = row.find(class_='table__team-name').get_text().strip()
            games = row.find(class_='table__cell--games-number').get_text().strip()
            wins = row.find(class_='table__cell--wins').get_text().strip()
            draws = row.find(class_='table__cell--draws').get_text().strip()
            losses = row.find(class_='table__cell--losses').get_text().strip()

            goals_strings = row.find(class_='table__cell--goals-scored_goals-missed').get_text().strip()
            goals_scored, goals_conceded = [int(goals.strip()) for goals in goals_strings.split('-')]

            points = row.find(class_='table__cell--points').get_text().strip()
            
            last_matches = row.find_all(class_='form-results-item')
            results = []

            # TODO: this parses wrong data
            for match in last_matches:
                if 'form-results-item--win' in match['class']:
                    results.append('W')
                if 'form-results-item--loss' in match['class']:
                    results.append('L')
                else:
                    results.append('D')

            teams.append({
                # TEAM
                'logo_url': logo_url,
                'name': name,
                # TEAM INFO
                'place': int(place),
                'games': int(games),
                'wins': int(wins),
                'draws': int(draws),
                'losses': int(losses),
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded,
                'points': int(''.join(i for i in points if i.isdigit())),
                # 'results': results
            })
        return teams

    def refresh_scoreboard(self):
        teams = self.get_scoreboard()
        league = League.objects.filter(active=True).first()
        for data in teams:
            teams = Team.objects.filter(name=data.get('name').lower())
            name = data.pop('name')
            logo_url = data.pop('logo_url')
            # create team if not created yet
            if not teams.exists():
                team = Team.objects.create(name=name, logo_url=logo_url)
            else:
                team = teams.first()

            infos = TeamInfo.objects.filter(team=team, league=league)
            # create teaminfo for current active league if not created yet
            if not infos.exists():
                data['league'] = league
                data['team'] = team
                TeamInfo.objects.create(**data)
            else:
                infos.update(**data)