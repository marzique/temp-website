from django.urls import path
from forecasts.views import (
    ForecastDetailView, 
    ForecastListView, 
    PredictView, 
    UpdatePointsView,
    ResetPredictionView
)

urlpatterns = [
    path('', ForecastListView.as_view(), name='forecast-list'),
    path('<int:pk>/', ForecastDetailView.as_view(), name='forecast-detail'),
    path('<int:pk>/predict/', PredictView.as_view(), name='predict'),
    path('<int:pk>/update_points/', UpdatePointsView.as_view(), name='update-points'),
    path('<int:pk>/reset/', ResetPredictionView.as_view(), name='reset-prediction'),
]