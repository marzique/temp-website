from social_django.models import UserSocialAuth

from django.db.models.signals import post_save
from django.dispatch import receiver

from users.utils import set_user_avatar_from_url, transliterate_user


@receiver(post_save, sender=UserSocialAuth)
def on_booking_delete(sender, instance, **kwargs):
    social = instance
    user = social.user
    picture_url = social.extra_data.get('picture', {}).get('data', {}).get('url')
    if picture_url and not user.profile.avatar:
        set_user_avatar_from_url(user, picture_url)
    transliterate_user(user)
