# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Anunciante

class CadastroForm(forms.Form):
    # Campos do Usuário (Obrigatórios para todos)
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: João'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Silva'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Pergunta chave
    is_anunciante = forms.BooleanField(
        label="Quero anunciar imóveis", 
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'checkAnunciante'})
    )

    # Campos do Anunciante (Opcionais no form, validados depois)
    telefone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control phone-mask', 'placeholder': '(00) 00000-0000'}))
    creci = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional para proprietários'}))
    bairro_atuacao = forms.CharField(required=False, label="Bairro de Atuação", widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        is_anunciante = cleaned_data.get("is_anunciante")

        # Valida senhas iguais
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não conferem.")

        # Validação condicional: Se marcou "Quero Anunciar", Telefone vira obrigatório
        if is_anunciante:
            if not cleaned_data.get('telefone'):
                self.add_error('telefone', "Telefone é obrigatório para anunciantes.")
            # CRECI pode continuar opcional (ex: proprietário direto), ou você obriga aqui se quiser.
        
        return cleaned_data
        

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