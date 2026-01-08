# imoveis/views.py
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Imovel

def index(request):
    # --- DEBUG: Vamos ver no terminal o que está chegando ---
    print(f"Ordem solicitada: {request.GET.get('order')}")
    
    # 1. ORDENAÇÃO
    # Se não vier nada na URL, usa '-id' (Mais Recente)
    order = request.GET.get('order', '-id')
    imoveis = Imovel.objects.filter(status='ATIVO').order_by(order)
    
    # 2. FILTROS
    cidade_busca = request.GET.get('cidade')
    if cidade_busca:
        imoveis = imoveis.filter(
            Q(cidade__icontains=cidade_busca) | 
            Q(bairro__icontains=cidade_busca)
        )
    
    tipo_busca = request.GET.get('tipo')
    if tipo_busca:
        imoveis = imoveis.filter(tipo_imovel=tipo_busca)
        
    finalidade_busca = request.GET.get('finalidade')
    if finalidade_busca:
        imoveis = imoveis.filter(tipo_transacao=finalidade_busca)

    # 3. FILTRO DE PREÇO
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if preco_min:
        imoveis = imoveis.filter(preco__gte=preco_min)
    
    if preco_max:
        imoveis = imoveis.filter(preco__lte=preco_max)

    # 4. PAGINAÇÃO
    paginator = Paginator(imoveis, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'index.html', context)