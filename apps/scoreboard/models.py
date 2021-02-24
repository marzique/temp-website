import re
from django.db import models


class Team(models.Model):
    PLACE_CHOICES = zip(range(1, 100), range(1, 100)) # 1-99

    place = models.PositiveIntegerField(choices=PLACE_CHOICES, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    logo_url = models.CharField(max_length=300)
    games = models.PositiveIntegerField(null=False, blank=False)
    wins = models.PositiveIntegerField(null=False, blank=False)
    draws = models.PositiveIntegerField(null=False, blank=False)
    losses = models.PositiveIntegerField(null=False, blank=False)
    goals_scored = models.PositiveIntegerField(null=False, blank=False)
    goals_conceded = models.PositiveIntegerField(null=False, blank=False)
    points = models.PositiveIntegerField(null=False, blank=False)
    
    class Meta:
        ordering = ['place']

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def alias(self):
        """Return team name alias:
        1) abbreviation - if more than 2 words OR
        2) strip everything except name inside quotes
        """
        
        words = self.name.split()
        
        if '"' in self.name:
            quoted = re.compile('"[^"]*"')
            return quoted.findall(self.name)[0][1:-1]
        elif len(words) > 2:
            if self.name.lower().startswith(('fc', 'фк')):
                return self.name[2:]
            return ''.join([word[0] for word in words])
        return self.name


class League(models.Model):
    name = models.CharField(max_length=64)
    years = models.CharField(max_length=9, null=False, blank=False)  # e.g. 2020 or 2021/2022
    active = models.BooleanField(default=True)

    class Meta:
        # One like per Post/Comment
        unique_together = (('name', 'years'),)

    def __str__(self):
        return f'{self.name} {self.years}'


class TeamInfo(models.Model):
    team = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        related_name='participates'
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='teams'
    )

    PLACE_CHOICES = zip(range(1, 100), range(1, 100)) # 1-99

    place = models.PositiveIntegerField(choices=PLACE_CHOICES, null=False, blank=False, default=0)
    games = models.PositiveIntegerField(null=False, blank=False, default=0)
    wins = models.PositiveIntegerField(null=False, blank=False, default=0)
    draws = models.PositiveIntegerField(null=False, blank=False, default=0)
    losses = models.PositiveIntegerField(null=False, blank=False, default=0)
    goals_scored = models.PositiveIntegerField(null=False, blank=False, default=0)
    goals_conceded = models.PositiveIntegerField(null=False, blank=False, default=0)
    points = models.PositiveIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f'{self.team} {self.league} [#{self.place}]'


class Match(models.Model):
    home = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        related_name='home_matches'
    )
    guest = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        related_name='away_matches'
    )
    score = models.CharField(max_length=6, default='-')
    link = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    league = models.CharField(max_length=20, default='HFL')
    next = models.BooleanField(default=None, unique=True, null=True)
    prev = models.BooleanField(default=None, unique=True, null=True)

    def __str__(self):
        return f'{self.home.name} {self.score} {self.guest.name}' 

    def save(self, *args, **kwargs):
        # make bools next & prev True only for one Match
        if self.next is False:
            self.next = None
        if self.prev is False:
            self.prev = None
        super().save(*args, **kwargs)
