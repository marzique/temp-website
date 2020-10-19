from django.urls import path
from scoreboard.views import ScoreboardView

urlpatterns = [
    path('', ScoreboardView.as_view(), name='scoreboard'),
]