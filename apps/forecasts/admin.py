from django.contrib import admin
from django.utils.html import format_html

from forecasts.models import Forecast, Season, Fixture, Prediction


class FixtureInline(admin.TabularInline):
    model = Fixture
    min_num = 0


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('week', 'season', 'status', 'created_at')

    inlines = [FixtureInline, ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'finished', 'created_at')
    list_filter = ('forecast',)



@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'forecast', 'with_teams', 'created_at')
    readonly_fields = ('created_at', )


    def with_teams(self, obj):
        new_results = []
        
        for week, goals in obj.results.items():
            fixture = Fixture.objects.get(id=week)
            home = fixture.get_home_name()
            guest = fixture.get_guest_name()
            new_results.append(
                f'{home} {goals[0]}:{goals[1]} {guest}'
            )
            
        return format_html('<br>'.join(new_results))
