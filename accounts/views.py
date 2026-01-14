# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Anunciante, Plano
from .forms import CadastroForm

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # 1. Cria o Usuário
            user = User.objects.create_user(
                username=form.cleaned_data['email'], # Usa o email como username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # 2. Cria o Perfil de Anunciante
            # Tenta pegar o plano GRATIS/START, se não existir, pega o primeiro que achar
            plano_padrao = Plano.objects.filter(nome='START').first() or Plano.objects.first()
            
            Anunciante.objects.create(
                user=user,
                telefone=form.cleaned_data['telefone'],
                creci=form.cleaned_data['creci'],
                bairro_atuacao=form.cleaned_data['bairro_atuacao'],
                plano=plano_padrao
            )
            
            # 3. Loga o usuário e manda pro Dashboard
            login(request, user)
            return redirect('dashboard')
    else:
        form = CadastroForm()
    
    return render(request, 'accounts/cadastro.html', {'form': form})

@login_required
def dashboard(request):
    # Pega os imóveis do usuário logado
    meus_imoveis = request.user.anunciante_profile.imoveis.all()
    
    context = {
        'imoveis': meus_imoveis
    }
    return render(request, 'accounts/dashboard.html', context)