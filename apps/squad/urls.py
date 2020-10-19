from django.urls import path
from squad.views import PlayerListView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player-list'),
]