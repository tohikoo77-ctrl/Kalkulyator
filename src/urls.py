from django.urls import path
from src.api_view import CalculatorAPI
from .views import home


urlpatterns = [
    path('calc/', CalculatorAPI.as_view()),
    path("home/", home,name="home")


]
