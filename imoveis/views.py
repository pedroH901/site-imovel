# imoveis/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Imovel, ImovelImagem
from .forms import ImovelForm, LeadForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

# --- VIEWS PÚBLICAS ---

def index(request):
    imoveis = Imovel.objects.filter(status='ATIVO').order_by('-id')[:6]
    context = {'page_obj': imoveis}
    return render(request, 'index.html', context)

def catalogo(request):
    imoveis = Imovel.objects.filter(status='ATIVO')
    
    # Filtros
    cidade = request.GET.get('cidade')
    if cidade:
        imoveis = imoveis.filter(Q(cidade__icontains=cidade) | Q(bairro__icontains=cidade))
    
    tipo = request.GET.get('tipo')
    if tipo:
        imoveis = imoveis.filter(tipo_imovel=tipo)
        
    finalidade = request.GET.get('finalidade')
    if finalidade:
        imoveis = imoveis.filter(tipo_transacao=finalidade)
        
    preco_min = request.GET.get('preco_min')
    if preco_min:
        imoveis = imoveis.filter(preco__gte=preco_min)
        
    preco_max = request.GET.get('preco_max')
    if preco_max:
        imoveis = imoveis.filter(preco__lte=preco_max)

    # Ordenação
    order = request.GET.get('order')
    if not order:
        order = '-id'
    imoveis = imoveis.order_by(order)

    # Paginação
    paginator = Paginator(imoveis, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'imoveis/catalogo.html', {'page_obj': page_obj})

def detalhe_imovel(request, slug):
    imovel = get_object_or_404(Imovel, slug=slug)
    
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.imovel = imovel
            lead.save()
            messages.success(request, 'Sua mensagem foi enviada com sucesso! O anunciante entrará em contato.')
            return redirect('detalhe_imovel', slug=slug)
    else:
        form = LeadForm()

    relacionados = Imovel.objects.filter(status='ATIVO', bairro=imovel.bairro).exclude(id=imovel.id)[:3]
    
    context = {
        'imovel': imovel,
        'relacionados': relacionados,
        'form': form
    }
    return render(request, 'detalhe_imovel.html', context)


# --- VIEWS DE FAVORITOS ---

def favoritos(request):
    return render(request, 'imoveis/favoritos.html')

def listar_favoritos_ids(request):
    ids_str = request.GET.get('ids', '')
    if not ids_str:
        return render(request, 'imoveis/partials/lista_cards.html', {'imoveis': []})
    
    try:
        ids = [int(i) for i in ids_str.split(',') if i.isdigit()]
        imoveis = Imovel.objects.filter(id__in=ids, status='ATIVO')
    except:
        imoveis = []
    
    return render(request, 'imoveis/partials/lista_cards.html', {'imoveis': imoveis})


# --- VIEWS DO ANUNCIANTE (BLINDADAS) ---

@login_required
def cadastrar_imovel(request):
    # BLINDAGEM: Se não for anunciante, chuta pro dashboard comum
    if not hasattr(request.user, 'anunciante_profile'):
        messages.error(request, "Apenas anunciantes podem cadastrar imóveis.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.anunciante = request.user.anunciante_profile
            imovel.save()
            
            # Salvar Múltiplas Imagens
            imagens = request.FILES.getlist('imagens_extras')
            for f in imagens:
                ImovelImagem.objects.create(imovel=imovel, imagem=f)
            
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('dashboard')
    else:
        form = ImovelForm()
    
    return render(request, 'imoveis/form_imovel.html', {'form': form})

@login_required
def editar_imovel(request, pk):
    # Busca o imóvel e GARANTE que pertence ao usuário logado (segurança extra)
    # Se o usuário não for dono ou não for anunciante, vai dar 404
    if not hasattr(request.user, 'anunciante_profile'):
        return redirect('dashboard')

    imovel = get_object_or_404(Imovel, id=pk, anunciante=request.user.anunciante_profile)
    
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            form.save()
            
            novas_imagens = request.FILES.getlist('imagens_extras')
            for f in novas_imagens:
                ImovelImagem.objects.create(imovel=imovel, imagem=f)
                
            messages.success(request, 'Imóvel atualizado!')
            return redirect('dashboard')
    else:
        form = ImovelForm(instance=imovel)
        
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'imovel': imovel})

@login_required
def excluir_imovel(request, pk):
    if not hasattr(request.user, 'anunciante_profile'):
        return redirect('dashboard')

    imovel = get_object_or_404(Imovel, id=pk, anunciante=request.user.anunciante_profile)
    imovel.delete()
    messages.success(request, 'Imóvel excluído com sucesso.')
    return redirect('dashboard')

@login_required
def remover_imagem(request, imagem_id):
    # Aqui precisamos de um cuidado extra: verificar se a imagem pertence a um imóvel do usuário
    imagem = get_object_or_404(ImovelImagem, id=imagem_id)
    
    # Verifica se o dono do imóvel é o usuário logado
    if imagem.imovel.anunciante.user != request.user:
        messages.error(request, "Você não tem permissão para fazer isso.")
        return redirect('dashboard')
        
    imovel_id = imagem.imovel.id
    imagem.delete()
    messages.success(request, "Imagem removida.")
    return redirect('editar_imovel', pk=imovel_id)