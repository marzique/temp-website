from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

from core.models import Timestamps


class PrivacyPolicy(Timestamps):
    text = RichTextUploadingField(blank=False, null=False)
    image = models.ImageField(upload_to='privacy/', blank=False, null=False)
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:50]
