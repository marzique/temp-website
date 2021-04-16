import requests
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError

from tempfile import NamedTemporaryFile

from django.core.files import File


def set_user_avatar_from_url(user, url):
    """
    Saves image from url as profile picture of user.
    """
    response = requests.get(url)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()
    try:
        user.profile.avatar.save(f"fb_avatar_{user.pk}", File(img_temp), save=True)
        return True
    except:
        return False


def transliterate_user(user):
    """
    Update username if no email from fb, and name is cyrillic.
    """
    social = user.social_auth.first()
    if social:
        
        name = social.extra_data.get('name')
        if not social.extra_data.get('email') and name:
            try:
                user.username = translit(name, reversed=True)
                user.save()
                return True
            except LanguageDetectionError:
                pass
    return False
