from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from squad.models import Player

class PlayerListView(ListView):
    model = Player
    ordering = ['position', 'number', ]


class PlayerDetailView(DetailView):
    model = Player
    slug_field = 'name_slug'
    slug_url_kwarg = 'name_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra'] = 'test'
        return context
