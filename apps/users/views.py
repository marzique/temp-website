
from django.views.generic.edit import CreateView
from django.urls import reverse

from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')