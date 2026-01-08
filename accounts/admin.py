# accounts/admin.py
from django.contrib import admin
from .models import Anunciante, Plano

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'max_imoveis')

@admin.register(Anunciante)
class AnuncianteAdmin(admin.ModelAdmin):
    list_display = ('user', 'plano', 'telefone', 'aprovado')
    list_filter = ('aprovado', 'plano')
    search_fields = ('user__username', 'user__email', 'creci')
    list_editable = ('aprovado', 'plano') # Aprova com um clique