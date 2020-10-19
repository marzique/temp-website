from django.urls import path
from main.views import AboutView

urlpatterns = [
    path('', AboutView.as_view(), name='index'),
]