from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator

from aboutconfig.models import Config

from scoreboard.models import Match
from scoreboard.services import HFLScoreboardService
from scoreboard.services import get_latest_league_context, update_teams_medals
from blog.models import Blog
from squad.services import get_today_birthday_players


@method_decorator(csrf_exempt, name='dispatch')
class MainPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scoreboard'] = get_latest_league_context()
        context['next_match'] = Match.objects.filter(next=True).first()
        context['prev_match'] = Match.objects.filter(prev=True).first()
        context['last_posts'] = Blog.objects.select_related('category').with_likes().filter(posted__lte=timezone.localtime(timezone.now())).order_by('-posted')[:3]
        context['birthdays'] = get_today_birthday_players()
        return context

    @transaction.atomic
    def refresh_scoreboard(self):
        HFLScoreboardService().refresh_scoreboard()
        update_teams_medals()
        self._update_scoreboard_timestamp()
    
    @staticmethod
    def _update_scoreboard_timestamp():
        updated_at = Config.objects.filter(key='scoreboard.updated_at')
        updated_at.update(
            value=timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        self.refresh_scoreboard()
        self.update_matches()
        return HttpResponseRedirect(reverse('index'))

    @transaction.atomic
    def update_matches(self):
        Match.objects.update_matches()
