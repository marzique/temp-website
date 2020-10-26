from django.contrib.auth.models import User
from scoreboard.models import Team
from django.db import models
from django.db.models import Count, Q, Min, Max, F
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver


class ProfileManager(models.Manager):
    pass


class ProfileQueryset(models.QuerySet):

    def with_predictions(self):
        qs = self.annotate(predictions_total=Count('predictions'))
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

    def calculate_total_points(self):
        """Calculate total points earned from all weeks"""
        points_total = 0
        for forecast, points in self.forecasts_points.items():
            points_total += points
            print(forecast, points)
        return points_total
    
    def create_or_update_points(self, forecast_id, week_points):
        # without str() forecasts_points JSONfield gets 2 keys both string and integer
        self.forecasts_points[str(forecast_id)] = week_points
        self.save()


# Create profiles for users automatically
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

