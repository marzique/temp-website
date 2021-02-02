from django.shortcuts import redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.utils import timezone

from forecasts.models import Forecast, Prediction, Season
from users.models import Profile


class ForecastDetailView(DetailView):
    queryset = Forecast.objects.prefetch_related(
        'predictions', 
        'predictions__user', 
        'fixtures__home',
        'fixtures__guest',
        ).all()
    template_name = 'forecasts/forecast_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Trigger forecast status change when user requests page after deadline
        if timezone.now() >= self.object.deadline and self.object.status == Forecast.ACTIVE:
            self.object.status = Forecast.STARTED
            self.object.save()

        if self.request.user.is_authenticated:
            context['can_vote'] = self._can_vote(**kwargs)

            if self._voted(**kwargs):
                user = self.request.user.profile
                results = Prediction.objects.select_related('user').get(user=user, forecast__pk=self.kwargs['pk']).results
                context['results'] = self._results_to_int_keys(results)
            
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
        Didn't vote yet, and this forecast is active.
        """

        if not self._voted(**kwargs):
            if self.get_object().status == Forecast.ACTIVE:
                return True
        return False


class ForecastListView(ListView):
    queryset = Forecast.objects.select_related('season').filter(season__archived=False)
    template_name = 'forecasts/forecast_list.html'

    def get_context_data(self, **kwargs):
        average = self.request.GET.get('average', False)
        if average:
            average = True

        context = super().get_context_data(**kwargs)
        
        context['user_profiles'] = self._get_top_predictors(average=average)
        context['average'] = average
        return context
    
    def _get_top_predictors(self, average=False, total=10):
        """
        Return `total` user profiles with at least 1 prediction,
        from latest not archived `season`.
        """

        profiles = Profile.objects.exclude(predictions__isnull=True).with_predictions().select_related('user')

        # reorder profiles by average points using plain python
        if average:
            return sorted(profiles, key=lambda a: a.average_points, reverse=True)

        return profiles.order_by('-total_points', 'predictions_total')
    

class PredictView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        prediction = self._compose_prediction(request)
        forecast_id = self.kwargs['pk']
        Prediction.objects.create(
            user=request.user.profile,
            forecast=Forecast.objects.get(pk=forecast_id),
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


class UpdatePointsView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        forecast_id = self.kwargs['pk']
        forecast = Forecast.objects.get(pk=forecast_id)
        forecast.update_profile_points()
        # change status if all matches are finished 
        if all(forecast.fixtures.values_list('finished', flat=True)):
            forecast.status = forecast.CALCULATED
            forecast.save()
        return redirect('forecast-detail', pk=forecast_id)


class ResetPredictionView(View):
    """Delete prediction of user for forecast"""

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        forecast_id = self.kwargs['pk']
        forecast = Forecast.objects.get(pk=forecast_id)
        prediction = Prediction.objects.get(user=profile, forecast=forecast)
        prediction.delete()

        return redirect('forecast-detail', pk=forecast_id)
