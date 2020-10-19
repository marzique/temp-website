from django.db import models


class Team(models.Model):
    PLACE_CHOICES = zip(range(1, 100), range(1, 100)) # 1-99

    place = models.PositiveIntegerField(choices=PLACE_CHOICES, null=False, blank=False, unique=True)
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

