# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Anunciante
from .models import Anunciante

class CadastroForm(forms.ModelForm):
    # Campos do User (Django)
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu Nome'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu Sobrenome'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha segura'}))
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}))

    # Campos do Anunciante (Nosso Model)
    telefone = forms.CharField(label="WhatsApp", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}))
    creci = forms.CharField(label="CRECI (Opcional)", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se for corretor'}))
    bairro_atuacao = forms.CharField(label="Bairro de Atuação", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tatuapé'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não conferem.")
        

class EditarPerfilForm(forms.ModelForm):
    # Campos do User (Nome e Sobrenome)
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})) # Email geralmente não deixamos mudar fácil pra não quebrar login

    class Meta:
        model = Anunciante
        # Campos do Anunciante
        fields = ['telefone', 'creci', 'bairro_atuacao', 'bio']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'creci': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro_atuacao': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }