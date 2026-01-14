# imoveis/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Imovel, ImovelImagem
from .forms import ImovelForm

def index(request):
    # 1. ORDENAÇÃO (Correção do Bug)
    order = request.GET.get('order')
    
    # Se 'order' não existir ou for vazio string vazia '', usa o padrão '-id'
    if not order:
        order = '-id'
        
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
    
    context = {'page_obj': page_obj}
    
    return render(request, 'index.html', context)

def detalhe_imovel(request, slug):
    imovel = get_object_or_404(Imovel, slug=slug)
    
    # Sugestão de "Veja Também" (Mesmo bairro, excluindo o atual)
    relacionados = Imovel.objects.filter(
        status='ATIVO', 
        bairro=imovel.bairro
    ).exclude(id=imovel.id)[:3]
    
    context = {
        'imovel': imovel,
        'relacionados': relacionados
    }
    return render(request, 'detalhe_imovel.html', context)
    
@login_required
def cadastrar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Salva o Imóvel (mas não commitado ainda, pois falta o anunciante)
            imovel = form.save(commit=False)
            imovel.anunciante = request.user.anunciante_profile
            imovel.save() # Agora salva com ID e Anunciante
            
            # 2. Processa as Imagens Múltiplas
            imagens = request.FILES.getlist('imagens')
            for img in imagens:
                ImovelImagem.objects.create(imovel=imovel, imagem=img)
            
            return redirect('dashboard')
    else:
        form = ImovelForm()
    
    return render(request, 'imoveis/form_imovel.html', {'form': form})

@login_required
def remover_imagem(request, imagem_id):
    # Busca a imagem, mas só se ela pertencer a um imóvel do usuário logado (Segurança!)
    imagem = get_object_or_404(ImovelImagem, id=imagem_id, imovel__anunciante=request.user.anunciante_profile)
    
    imovel_id = imagem.imovel.id # Guarda o ID para voltar depois
    imagem.delete() # Apaga do banco e da pasta (graças ao signals.py)
    
    # Volta para a tela de edição desse imóvel
    return redirect('editar_imovel', pk=imovel_id)

@login_required
def editar_imovel(request, pk):
    # Garante que o imóvel existe e pertence ao usuário logado
    imovel = get_object_or_404(Imovel, pk=pk, anunciante=request.user.anunciante_profile)
    
    if request.method == 'POST':
        # Passamos 'instance=imovel' para o form saber que é uma edição, não criação
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            imovel = form.save()
            
            # Adiciona NOVAS fotos (sem apagar as antigas)
            imagens = request.FILES.getlist('imagens')
            for img in imagens:
                ImovelImagem.objects.create(imovel=imovel, imagem=img)
            
            return redirect('dashboard')
    else:
        form = ImovelForm(instance=imovel)
    
    # Passamos o imóvel também para poder listar as fotos antigas no HTML
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'imovel': imovel})

@login_required
def excluir_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk, anunciante=request.user.anunciante_profile)
    imovel.delete()
    return redirect('dashboard')