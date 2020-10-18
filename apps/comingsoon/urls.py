from django.urls import path
from comingsoon import views

urlpatterns = [
    path('', views.comingsoon, name='comingsoon'),
]
