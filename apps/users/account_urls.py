from django.urls import path

from users.views import (
    AccountView,
    EditUserProfileView
)


urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('update/', EditUserProfileView.as_view(), name='account-update')
]
