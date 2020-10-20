from django.urls import path
from squad.views import PlayerListView, PlayerDetailView, LineupGeneratorView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player-list'),
    path('lineup/', LineupGeneratorView.as_view(), name='lineup'),
    path('<slug:name_slug>/', PlayerDetailView.as_view(), name='player-detail'),
]