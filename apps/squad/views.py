from django.utils import timezone
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, FileResponse, HttpResponse
from django.db import transaction

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


class LineupGeneratorView(ListView):
    model = Player
    ordering = ['number']
    template_name = 'squad/lineup.html'


@method_decorator(csrf_exempt, name='dispatch')
class LineupDownloadView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        # return FileResponse(open('myfile.png', 'rb'))
        table = request.POST.get('table_html')
        
        return HttpResponse('test')

