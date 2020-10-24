from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

from scoreboard.models import Team
from users.models import Profile


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

    @property
    def deadline(self):
        """Return datetime of the first match -1 hour"""
        
        first_match_date = self.fixtures.filter(date__isnull=False).earliest('date')
        return first_match_date.date - timedelta(hours=1)

    def __str__(self):
        return f'{self.season} Week {self.week}'



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

    def __str__(self):
        return f'{self.get_home_name()} {self.home_goals}:{self.guest_goals} {self.get_guest_name()}'

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
        #One gameweek forecast per user
        unique_together = ('user', 'forecast')

    def __str__(self):
        return f'{self.user} {self.forecast}'
