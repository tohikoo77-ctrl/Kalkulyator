from django.urls import path
from src.api_view import CalculatorAPI, GeminiKalkulator
from .views import home


urlpatterns = [

    path('api/calc/', CalculatorAPI.as_view(), name='calc_api'),


    path('api/gemini/', GeminiKalkulator.as_view(), name='gemini_api'),


    path('home/', home, name='home'),

    path('', home, name='index'),
]
