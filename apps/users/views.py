
from django.views.generic.edit import CreateView
from django.urls import reverse

from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


# TODO: Inherit default auth views and override labels and stuff
# https://stackoverflow.com/questions/53980603/is-there-any-way-to-change-username-field-label-in-user-authentication-login-pag
