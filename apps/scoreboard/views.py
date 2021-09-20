from django.views.generic import TemplateView

from scoreboard.utils import get_latest_league_context


class ScoreboardView(TemplateView):
    template_name = "scoreboard/scoreboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.refresh_scoreboard()
        context['scoreboard'] = get_latest_league_context()
        return context
