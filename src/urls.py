from django.urls import path
from src.api_view import Kalkulator


urlpatterns = [
    path('calc/', Kalkulator.as_view())
]
