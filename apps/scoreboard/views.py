from django.views.generic import TemplateView


class ScoreboardView(TemplateView):
    template_name = "scoreboard.html"
