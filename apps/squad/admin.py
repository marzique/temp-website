from django.contrib import admin

from squad.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('number', 'position', 'name', 'captain')

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
