from django.urls import path
from users.views import RegisterView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
]