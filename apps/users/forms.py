from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UsernameField, 
    UserCreationForm
)
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from users.models import Profile 


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, label='Нікнейм')
    first_name = forms.CharField(required=True, label='Ім\'я')
    last_name = forms.CharField(required=True, label='Прізвище')
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Введіть такий самий пароль для валідації",
    )

    class Meta:
         model = User
         fields = ('first_name', 'last_name', 
                    'email', 'username',  'password1', 'password2')


    def save(self, commit=True):
        # Call save of the super of your own class,
        # which is UserCreationForm.save() which calls user.set_password()
        user = super().save(commit=False) 

        # Add the things your super doesn't do for you
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Overwrite field labels"""
    username = UsernameField(
        label='Логін або email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput,
    )


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    avatar = forms.FileField()
    
    class Meta:
        model = Profile
        fields = ('avatar', )
