# imoveis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # A rota vazia '' significa a página inicial
]