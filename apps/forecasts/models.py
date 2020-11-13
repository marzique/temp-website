from datetime import timedelta

from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from scoreboard.models import Team
from users.models import Profile
from forecasts.constants import (
    WIN_OR_DRAW_POINTS, 
    WIN_AND_ONE_SIDE_GOALS_POINTS, 
    EXACT_SCORE_POINTS
)


class Forecast(models.Model):

    ACTIVE = 1
    STARTED = 2
    CALCULATED = 3

    STATUSES = (
        (ACTIVE, 'Прийом ставок'),
        (STARTED, 'Тур розпочався'),
        (CALCULATED, 'Очки зараховані'),
    )

    season = models.ForeignKey('forecasts.Season', on_delete=models.CASCADE)
    week = models.PositiveIntegerField()
    status = models.PositiveIntegerField(choices=STATUSES, null=False, blank=False, default=ACTIVE)
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def deadline(self):
        """Return datetime of the first match -1 hour"""
        
        first_match_date = self.fixtures.filter(date__isnull=False).earliest('date')
        return first_match_date.date - timedelta(hours=1)

    def __str__(self):
        return f'{self.season} Тур {self.week}'

    @transaction.atomic
    def update_profile_points(self):
        """
        Calculate points for every fixture prediction made by Users and update their profile's forecasts_points 
        dicts accordingly. Only finished fixtures taken into account. This method can be safely called multiple times.
        """

        for prediction in self.predictions.all():
            week_points = 0
            profile = prediction.user
            for fixture_id, predicted_score in prediction.results.items():
                fixture = Fixture.objects.get(id=fixture_id)
                # allow partially finished Forecasts calculations
                if fixture.finished:
                    points = self.calculate_fixture_prediction(fixture, predicted_score)
                    week_points += points
            profile.create_or_update_points(self.id, week_points)


    def calculate_fixture_prediction(self, fixture, predicted_score):
        winner = self.get_winner_from_score(fixture.score)
        predicted_winner = self.get_winner_from_score(predicted_score)
        # at least 5 points
        if winner == predicted_winner:
            matches = self.matched_goals_both(fixture.score, predicted_score)
            if matches == 2:
                return EXACT_SCORE_POINTS
            if matches == 1:
                return WIN_AND_ONE_SIDE_GOALS_POINTS
            return WIN_OR_DRAW_POINTS
        else:
            return 0

    def get_winner_from_score(self, score):
        if score[0] > score[1]:
            return 1
        elif score[0] < score[1]:
            return -1
        else:
            return 0

    def matched_goals_both(self, score1, score2):
        matched = 0
        for pair in zip(score1, score2):
            # pair has 2 same integers
            if pair[1:] == pair[:-1]:
                matched += 1
        return matched


class Season(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.name


class Fixture(models.Model):
    forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE, related_name='fixtures')
    home = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='home_fixtures'
    )
    guest = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='away_fixtures'
    )

    # backup fields for feature matches not from HFL scoreboard
    home_name = models.CharField(max_length=30, blank=True)
    home_logo = models.ImageField(upload_to='fixtures/', blank=True)
    guest_name = models.CharField(max_length=30, blank=True)
    guest_logo = models.ImageField(upload_to='fixtures/', blank=True)

    home_goals = models.PositiveIntegerField(null=True, blank=True)
    guest_goals = models.PositiveIntegerField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(blank=False, null=False)

    class Meta:
        ordering = ['date']

    def clean(self):
        # don't allow 'finish' match without goals
        if self.pk:
            if self.home_goals is None or self.guest_goals is None:
                if self.finished:
                    raise ValidationError('Provide goals if match is finished!')

    def save(self, *args, **kwargs):
        # recalculate total points each time profile saved
        if isinstance(self.home_goals, int) and isinstance(self.guest_goals, int):
            self.finished = True
        else:
            self.finished = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_home_name()} {self.home_goals}:{self.guest_goals} {self.get_guest_name()}'

    @property
    def score(self):
        return [self.home_goals, self.guest_goals]

    def get_home_name(self):
        if self.home:
            return self.home.alias
        else:
            return self.home_name

    def get_guest_name(self):
        if self.guest:
            return self.guest.alias
        else:
            return self.guest_name
    
    def get_home_logo_url(self):
        if self.home:
            return self.home.logo_url
        else:
            return self.home_logo.url

    def get_guest_logo_url(self):
        if self.guest:
            return self.guest.logo_url
        else:
            return self.guest_logo.url


class Prediction(models.Model):
    user = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        related_name='predictions'
    )
    forecast = models.ForeignKey(
        Forecast, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        related_name='predictions'
    )
    # {fixture_id: [1, 0], }
    results = models.JSONField(blank=False, null=False, default=dict)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One gameweek forecast per user
        unique_together = ('user', 'forecast')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} {self.forecast}'

    @property
    def points(self):
        return self.user.forecasts_points[str(self.forecast.id)]

    @property
    def fixtures(self):
        fixtures = []
        
        for week, goals in self.results.items():
            fixture = Fixture.objects.get(id=week)
            home_logo = fixture.get_home_logo_url()
            guest_logo = fixture.get_guest_logo_url()
            date = fixture.date
            fixtures.append({
                    'home_logo': home_logo,
                    'guest_logo': guest_logo,
                    'goals': goals,
                    'date': date
            })

        sorted_fixtures = sorted(fixtures, key=lambda k: k['date']) 
        return sorted_fixtures
            