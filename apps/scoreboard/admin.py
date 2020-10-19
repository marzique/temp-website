from django.contrib import admin

from scoreboard.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('place', 'name', 'points')
