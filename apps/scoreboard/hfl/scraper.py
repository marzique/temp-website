import requests
from bs4 import BeautifulSoup

from django.conf import settings


class HFLScoreBoardParser:
    def __init__(self):
        self.url = settings.HFL_SCOREBOARD_URL

    def _get_html(self):
        resp = requests.get(self.url)
        return resp.text

    def _extract_table(self):
        """Extract all rows with team stats from table"""

        html = self._get_html()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(id='tournaments-tables-table-1')
        rows = table.find_all(class_='table__row')
        return rows
    
    def get_scoreboard(self):
        rows = self._extract_table()

        teams = []
        for row in rows:
            place = row.find(class_='table__cell--number').get_text().strip()
            logo = row.find(class_='table__team-img').get('src')
            name = row.find(class_='table__team-name').get_text().strip()
            games = row.find(class_='table__cell--games-number').get_text().strip()
            wins = row.find(class_='table__cell--wins').get_text().strip()
            draws = row.find(class_='table__cell--draws').get_text().strip()
            losses = row.find(class_='table__cell--losses').get_text().strip()
            goals = row.find(class_='table__cell--goals-scored_goals-missed').get_text().strip()
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
                'place': place,
                'logo': logo,
                'name': name,
                'games': games,
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals': goals,
                'points': points,
                'results': results
            })
        return teams
             