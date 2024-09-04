from django.urls import path
from .views import PredictText, GetPredictions

urlpatterns = [
    path('predict/', PredictText.as_view(), name='predict_text'),
    path('predictions/', GetPredictions.as_view(), name='get_predictions'),
]