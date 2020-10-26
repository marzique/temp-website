from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


from users.forms import CustomUserCreationForm, CustomAuthenticationForm  


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
        user = self.request.user
        context['user'] = user
        return context
    