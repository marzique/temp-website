from django.contrib.auth.models import User
from scoreboard.models import Team
from django.db import models
from django.db.models import Count, Q, Min, Max, F
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileManager(models.Manager):
    pass


class ProfileQueryset(models.QuerySet):

    def with_predictions(self):
        qs = self.annotate(predictions_total=Count('predictions'))
        return qs



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forecast_points = models.IntegerField(default=0)
    favourite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)

    objects = ProfileManager.from_queryset(ProfileQueryset)()

    def __str__(self):
        return str(self.user)


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

