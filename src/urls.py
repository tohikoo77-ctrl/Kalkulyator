from django.urls import path
from .views import calculator_view, calculate_api, history_api

urlpatterns = [
    path('', calculator_view, name='home'),
    path('api/calculate/', calculate_api),
    path('api/history/', history_api),
]