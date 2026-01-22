# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from .models import Anunciante, Plano
from .forms import CadastroForm, EditarPerfilForm 
def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # 1. Cria o Usuário
            user = User.objects.create_user(
                username=form.cleaned_data['email'], 
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # 2. Cria o Perfil de Anunciante
            plano_padrao = Plano.objects.filter(nome='START').first() or Plano.objects.first()
            
            Anunciante.objects.create(
                user=user,
                telefone=form.cleaned_data['telefone'],
                creci=form.cleaned_data['creci'],
                bairro_atuacao=form.cleaned_data['bairro_atuacao'],
                plano=plano_padrao
            )
            
            # 3. Loga e redireciona
            login(request, user)
            return redirect('dashboard')
    else:
        form = CadastroForm()
    
    return render(request, 'accounts/cadastro.html', {'form': form})

# --- FUNÇÕES QUE FALTAVAM ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def dashboard(request):
    try:
        meus_imoveis = request.user.anunciante_profile.imoveis.all()
    except:
        meus_imoveis = [] # Previne erro se admin logar sem perfil de anunciante
        
    context = {
        'imoveis': meus_imoveis
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def editar_perfil(request):
    try:
        anunciante = request.user.anunciante_profile
    except:
        # Caso seja um superuser sem perfil, evita quebrar a página
        messages.error(request, "Seu usuário não possui perfil de anunciante.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=anunciante)
        
        if form.is_valid():
            form.save()
            
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('editar_perfil')
            
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = EditarPerfilForm(instance=anunciante, initial=initial_data)
    
    return render(request, 'accounts/editar_perfil.html', {'form': form})