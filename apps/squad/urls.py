from django.urls import path
from squad.views import PlayerListView, PlayerDetailView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player-list'),
    path('<slug:name_slug>/', PlayerDetailView.as_view(), name='player-detail'),
]