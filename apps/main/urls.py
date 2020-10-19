from django.urls import path
from main.views import MainPageView, RefreshScoreboardView

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('refresh-scoreboard', RefreshScoreboardView.as_view(), name='refresh-scoreboard'),
]