from django.shortcuts import redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from forecasts.models import Forecast, Prediction
from users.models import Profile


class ForecastDetailView(DetailView):
    model = Forecast
    template_name = 'forecasts/forecast_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['can_vote'] = self._can_vote(**kwargs)
            if self._voted(**kwargs):
                user = self.request.user.profile
                results = Prediction.objects.get(user=user, forecast__pk=self.kwargs['pk']).results
                context['results'] = self._results_to_int_keys(results)
                print(context['results'])

        return context

    def _results_to_int_keys(self, results):
        new_results = {}
        for k, v in results.items():
            new_results[int(k)] = v
        return new_results
    
    def _voted(self, **kwargs):
        """
        Check if user already voted this week.
        """
        user = self.request.user.profile
        return Prediction.objects.filter(user=user, forecast__pk=self.kwargs['pk']).exists()

    def _can_vote(self, **kwargs):
        """
        User can vote if:
        1) he is authenticated
        2) didn't vote this week
        3) forecast is active.
        """
        if not self._voted(**kwargs):
            if self.get_object().status == Forecast.ACTIVE:
                return True
        return False
        

class ForecastListView(ListView):
    model = Forecast
    template_name = 'forecasts/forecast_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profiles'] = Profile.objects.with_predictions()\
        .order_by('-forecast_points', 'predictions_total').select_related('user')[:10]
        return context
    

class PredictView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        prediction = self._compose_prediction(request)
        forecast_id = self.kwargs['pk']
        Prediction.objects.create(
            user=request.user.profile,
            forecast=Forecast.objects.get(),
            results=prediction
        )
        return redirect('forecast-detail', pk=forecast_id)

    def _compose_prediction(self, request):
        prediction = {}
        for k in request.POST:
            if k.startswith('fixture'):
                pk = k.replace('fixture', '')
                scores = request.POST.getlist(k)
                prediction[pk] = [int(goals) for goals in scores]
        return prediction