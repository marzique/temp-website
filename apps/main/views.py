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

from scoreboard.models import Team, Match
from scoreboard.hfl import HFLScoreBoardParser
from blog.models import Blog


@method_decorator(csrf_exempt, name='dispatch')
class MainPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['scoreboard'] = Team.objects.all()
        context['next_match'] = Match.objects.filter(next=True).first()
        context['prev_match'] = Match.objects.filter(prev=True).first()
        context['last_posts'] = Blog.objects.order_by('-posted')[:3]
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
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        self.refresh_scoreboard()
        self.update_matches()
        return HttpResponseRedirect(reverse('index'))

    @transaction.atomic
    def update_matches(self):
        future_matches = Match.objects.filter(date__gte=timezone.localtime(timezone.now()))
        tba_matches = Match.objects.filter(date__isnull=True)
        next_match = None
        if future_matches.exists():
            next_match = future_matches.latest('date')
        elif tba_matches.exists():
            next_match = tba_matches.latest('id')

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

