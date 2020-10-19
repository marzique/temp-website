from django.views.generic import TemplateView
from django.views import View
from django.db import transaction

from scoreboard.models import Team
from scoreboard.hfl import HFLScoreBoardParser

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
            team = Team.objects.filter(name=data.pop('name').lower())
            if team.exists():
                data.pop('logo_url')    
                team.update(**data)
            else:
                team = Team.objects.create(**data)


class RefreshScoreboardView(View):
    pass
