from django.contrib import admin

from scoreboard.models import Team, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'points', 'logo_url')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home', 'score', 'guest', 'next', 'prev', 'date')