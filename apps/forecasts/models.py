from datetime import timedelta

from django.db import models

from scoreboard.models import Team

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
    date = models.DateTimeField(blank=False, null=False)

    class Meta:
        ordering = ['date']

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
    pass
