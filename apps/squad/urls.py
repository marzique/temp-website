from django.urls import path
from squad.views import (
    PlayerListView, 
    PlayerDetailView, 
    LineupGeneratorView, 
    LineupDownloadView,
    SquadDetailView
)

urlpatterns = [
    path('', PlayerListView.as_view(), name='player-list'),
    path('lineup/', LineupGeneratorView.as_view(), name='lineup'),
    path('lineup/download/', LineupDownloadView.as_view(), name='lineup-download'),
    path('lineup/<slug:slug>/', SquadDetailView.as_view(), name='lineup-detail'),
    path('<slug:name_slug>/', PlayerDetailView.as_view(), name='player-detail'),
]