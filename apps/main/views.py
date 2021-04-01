from datetime import datetime, timedelta

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

from scoreboard.models import Team, Match, League, TeamInfo
from scoreboard.hfl import HFLScoreBoardParser
from scoreboard.utils import get_lates_league_context
from blog.models import Blog
from squad.models import Player
from squad.utils import get_todays_birthday_players


@method_decorator(csrf_exempt, name='dispatch')
class MainPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['scoreboard'] = get_lates_league_context()
        context['next_match'] = Match.objects.filter(next=True).first()
        context['prev_match'] = Match.objects.filter(prev=True).first()
        context['last_posts'] = Blog.objects.select_related('category').with_likes().filter(posted__lte=timezone.localtime(timezone.now())).order_by('-posted')[:3]
        context['birthdays'] = get_todays_birthday_players()
        return context

    @transaction.atomic
    def refresh_scoreboard(self):
        teams = HFLScoreBoardParser().get_scoreboard()
        league = League.objects.filter(active=True).first()
        for data in teams:
            teams = Team.objects.filter(name=data.get('name').lower())
            name = data.pop('name')
            logo_url = data.pop('logo_url')
            # create team if not created yet
            if not teams.exists():
                team = Team.objects.create(name=name, logo_url=logo_url)
            else:
                team = teams.first()

            infos = TeamInfo.objects.filter(team=team, league=league)
            # create teaminfo for current active league if not created yet
            if not infos.exists():
                data['league'] = league
                data['team'] = team
                info = TeamInfo.objects.create(**data)
            else:
                infos.update(**data)
        self._update_scoreboard_timestamp()
        
    
    def _update_scoreboard_timestamp(self):
        last_updated = Config.objects.get(key='scoreboard.updated_at')
        last_updated.value = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        last_updated.save()
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        self.refresh_scoreboard()
        self.update_matches()
        return HttpResponseRedirect(reverse('index'))

    @transaction.atomic
    def update_matches(self):
        Match.objects.update(next=None, prev=None)
        future_matches = Match.objects.filter(date__gte=timezone.localtime(timezone.now()))
        tba_matches = Match.objects.filter(date__isnull=True)
        next_match = None
        if future_matches.exists():
            next_match = future_matches.earliest('date')
        elif tba_matches.exists():
            next_match = tba_matches.earliest('id')

        prev_matches = Match.objects.filter(date__lt=timezone.localtime(timezone.now()))
        prev_match = None
        if prev_matches.exists():
            prev_match = prev_matches.latest('date')
        
        if next_match:
            next_match.next = True
            next_match.save()
        if prev_match:
            prev_match.prev = True
            prev_match.save()

