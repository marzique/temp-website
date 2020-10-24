from django.urls import path
from forecasts.views import ForecastDetailView, ForecastListView, PredictView

urlpatterns = [
    path('', ForecastListView.as_view(), name='forecast-list'),
    path('<int:pk>/', ForecastDetailView.as_view(), name='forecast-detail'),
    path('<int:pk>/predict/', PredictView.as_view(), name='predict'),
]