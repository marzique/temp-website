from django.contrib.auth.models import User
from scoreboard.models import Team
from forecasts.models import Season, Forecast
from django.db import models
from django.db.models import Count, Q, Min, Max, F
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver


class ProfileManager(models.Manager):
    pass


class ProfileQueryset(models.QuerySet):

    def with_predictions(self):
        season = Season.objects.filter(archived=False).order_by('created_at').first()
        qs = self.annotate(predictions_total=Count('predictions', filter=Q(predictions__forecast__season=season)))
        return qs


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # {forecast_id: points, }
    forecasts_points = models.JSONField(blank=True, null=True, default=dict)
    favourite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    total_points = models.PositiveIntegerField(default=0, editable=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    objects = ProfileManager.from_queryset(ProfileQueryset)()

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        # recalculate total points each time profile saved
        self.total_points = self.calculate_total_points()
        super().save(*args, **kwargs)

    def calculate_total_points(self, total=False):
        """Calculate total points earned from all weeks"""
        points_total = 0
        for forecast, points in self.forecasts_points.items():
            if int(forecast) in self.forecast_ids:
                points_total += points
        return points_total
    
    @property
    def forecast_ids(self, total=False):
        seasons = Season.objects.all()
        if not total:
            seasons = seasons.filter(archived=False)
        return Forecast.objects.filter(season__in=seasons).values_list('id', flat=True)

    @property
    def average_points(self):
        if self.forecasts_points and self.total_points:
            current_forecast_ids = [i for i in self.forecasts_points if int(i) in self.forecast_ids]
            return round(self.total_points / len(current_forecast_ids), 2)
        return 0
    
    def create_or_update_points(self, forecast_id, week_points):
        # without str() forecasts_points JSONfield gets 2 keys both string and integer
        self.forecasts_points[str(forecast_id)] = week_points
        self.save()


# Create profiles for users automatically
# Use user 'super' with pk 999 both in produciton and dev to be able
# to transfer data via smuggler
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
