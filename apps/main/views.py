from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from aboutconfig.models import Config

from scoreboard.models import Team
from scoreboard.hfl import HFLScoreBoardParser



@method_decorator(csrf_exempt, name='dispatch')
class MainPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.refresh_scoreboard()
        context['scoreboard'] = Team.objects.all()
        return context

    @transaction.atomic
    def refresh_scoreboard(self):
        teams = HFLScoreBoardParser().get_scoreboard()
        for data in teams:
            team = Team.objects.filter(name=data.get('name').lower())
            if team.exists():
                data.pop('name')
                data.pop('logo_url')    
                team.update(**data)
            else:
                team = Team.objects.create(**data)
        self._update_scoreboard_timestamp()
        
    
    def _update_scoreboard_timestamp(self):
        last_updated = Config.objects.get(key='scoreboard.updated_at')
        last_updated.value = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        last_updated.save()

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        self.refresh_scoreboard()
        return HttpResponseRedirect(reverse('index'))
