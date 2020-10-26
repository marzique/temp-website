from django.contrib import admin

from forecasts.models import Forecast, Season, Fixture, Prediction


class FixtureInline(admin.TabularInline):
    model = Fixture
    min_num = 0


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('week', 'season', 'status')

    inlines = [FixtureInline, ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'finished')
    list_filter = ('forecast',)



@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'forecast', 'results', 'created_at']
    readonly_fields = ['created_at', ]
