from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('', views.temp, name='temp'),
    path('home/', views.home, name='home'),
    path('extract/', views.extract, name='extract'),
]