from django.contrib import admin

from squad.models import Player, Squad

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('number', 'position', 'name', 'captain')
    readonly_fields = ['name_slug']

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    pass
