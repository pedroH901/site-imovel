# imoveis/admin.py
from django.contrib import admin
from .models import Imovel, ImovelImagem, Lead

# Isso permite adicionar várias fotos direto na tela do Imóvel
class ImovelImagemInline(admin.TabularInline):
    model = ImovelImagem
    extra = 1 # Quantos campos vazios aparecem por padrão

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    # O que aparece na lista
    list_display = ('titulo', 'bairro', 'preco', 'tipo_transacao', 'status', 'destaque')
    
    # Filtros laterais (baseado no que vimos no HTML)
    list_filter = ('status', 'tipo_imovel', 'tipo_transacao', 'cidade')
    
    # Barra de busca
    search_fields = ('titulo', 'bairro', 'cidade', 'descricao')
    
    # Campos que podem ser editados direto na lista (bom para aprovação rápida)
    list_editable = ('status', 'destaque')
    
    # Gera o slug automaticamente enquanto você digita o título
    prepopulated_fields = {'slug': ('titulo',)}
    
    # Adiciona as fotos
    inlines = [ImovelImagemInline]

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'nome', 'email', 'telefone', 'created_at', 'respondido')
    list_filter = ('respondido', 'created_at')
    search_fields = ('nome', 'email', 'imovel__titulo')
    list_editable = ('respondido',)