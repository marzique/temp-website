from django.contrib import admin

from squad.models import Player, Squad

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('number', 'position', 'name', 'captain', 'date_of_birth')
    readonly_fields = ['name_slug']

    def name(self, obj):
        return obj.full_name


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    pass
