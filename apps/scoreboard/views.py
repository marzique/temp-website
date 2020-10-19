from django.views.generic import TemplateView

from scoreboard.models import Team


class ScoreboardView(TemplateView):
    template_name = "scoreboard/scoreboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.refresh_scoreboard()
        context['scoreboard'] = Team.objects.all()
        return context
