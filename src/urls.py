from django.urls import path
from .views import calculator_view, calculate_api

urlpatterns = [
    path('', calculator_view, name='calculator'),
    path('api/calculate/', calculate_api),
]
