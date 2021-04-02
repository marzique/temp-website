from django.contrib import admin
from core.models import PrivacyPolicy


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'snippet', 'author', 'created_at', 'active')

    def snippet(self, obj):
        return obj.text[:30]
