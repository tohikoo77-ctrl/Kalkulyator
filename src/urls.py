from django.urls import path
from src.api_view import CalculatorAPI


urlpatterns = [
    path('calc/', CalculatorAPI.as_view())
]
