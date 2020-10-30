from django.db import transaction
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


from users.forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm,
    EditUserForm,
    EditProfileForm,
)
from users.models import Profile
from forecasts.models import Forecast, Prediction


class RegisterView(CreateView):
    """View to register a new user."""

    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class CustomLoginView(LoginView):
    """View to login using username or email (see users.authentication)"""

    template_name='auth/login.html'
    authentication_form = CustomAuthenticationForm


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name='auth/password_reset.html'


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass



### ACCOUNT VIEWS
class AccountView(LoginRequiredMixin, TemplateView):
    template_name='account/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self._get_forecasts_stats()
        context['place'] = self._get_place()
        return context

    def _get_forecasts_stats(self):
        user = self.request.user
        stats = {}

        predictions = Prediction.objects.select_related('user', 'forecast').filter(user=user.profile)
        for prediction in predictions:
            name = str(prediction.forecast)
            points_dict = user.profile.forecasts_points
            points = points_dict.get(str(prediction.forecast.id), 0)
            if not points:
                points_dict[str(prediction.forecast.id)] = 0
                user.save()
            stats[name] = points

        return stats

    def _get_place(self):
        return Profile.objects.filter(total_points__gt=self.request.user.profile.total_points).count() + 1
    

class EditUserProfileView(LoginRequiredMixin, View):
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = request.POST
        files = request.FILES
        user_form = EditUserForm(data, instance=user)
        profile_form = EditProfileForm(data, files, instance=user.profile)
        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()

        return HttpResponseRedirect(reverse('account'))

    def get_object(self, queryset=None):
        return self.request.user
