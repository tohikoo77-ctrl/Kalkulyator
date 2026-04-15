from django.urls import path
from src.api_view import Kalkulator
from .views import home


urlpatterns = [
    path('calc/', Kalkulator.as_view()),
    path("home/", home,name="home")

]
