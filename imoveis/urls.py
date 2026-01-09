from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('imovel/<slug:slug>/', views.detalhe_imovel, name='detalhe_imovel'),
]