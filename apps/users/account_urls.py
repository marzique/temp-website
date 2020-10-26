from django.urls import path

from users.views import (
    AccountView
)


urlpatterns = [
    path('', AccountView.as_view(), name='account'),
]
