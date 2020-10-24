from django.contrib import admin

from forecasts.models import Forecast, Season, Fixture, Prediction


class FixtureInline(admin.TabularInline):
    model = Fixture
    min_num = 0


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('season', 'week')

    inlines = [FixtureInline, ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    pass


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    pass
