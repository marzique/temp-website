from django.contrib import admin

from scoreboard.models import Team, Match, TeamInfo, League


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_url')


@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'place', 'points')
    list_filter = ('league', 'team')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home', 'score', 'guest', 'next', 'prev', 'date')


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'years', 'active')
    list_filter = ('active',)
