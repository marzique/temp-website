from django.urls import path
from forecasts.views import ForecastDetailView, ForecastListView

urlpatterns = [
    path('', ForecastListView.as_view(), name='forecast-list'),
    path('<int:pk>/', ForecastDetailView.as_view(), name='forecast-detail'),
]