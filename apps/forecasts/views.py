

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from forecasts.models import Forecast


class ForecastDetailView(DetailView):
    model = Forecast
    template_name = 'forecasts/forecast_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ForecastListView(ListView):
    model = Forecast
    template_name = 'forecasts/forecast_list.html'
