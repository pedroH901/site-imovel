# imoveis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    # Área do Anunciante
    path('imovel/criar/', views.cadastrar_imovel, name='cadastrar_imovel'),
    path('imovel/editar/<int:pk>/', views.editar_imovel, name='editar_imovel'),
    path('imovel/excluir/<int:pk>/', views.excluir_imovel, name='excluir_imovel'),
    path('imagem/remover/<int:imagem_id>/', views.remover_imagem, name='remover_imagem'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('favoritos/carregar/', views.listar_favoritos_ids, name='carregar_favoritos'),
    
    # Rotas Públicas
    path('imovel/<slug:slug>/', views.detalhe_imovel, name='detalhe_imovel'),
]