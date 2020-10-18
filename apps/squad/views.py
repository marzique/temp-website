from django.utils import timezone
from django.views.generic.list import ListView

from squad.models import Player

class PlayerListView(ListView):

    model = Player
    paginate_by = 10  # if pagination is desired
