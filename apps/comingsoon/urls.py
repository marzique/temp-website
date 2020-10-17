from django.urls import path
from comingsoon import views

urlpatterns = [
    path('', views.index, name='index'),
]
