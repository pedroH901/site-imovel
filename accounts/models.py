# accounts/models.py
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class Plano(TimeStampedModel):
    # Atualizamos as opções conforme a visão do CEO (Pessoa Física e Jurídica)
    NOME_CHOICES = (
        ('START', 'Start (Grátis 60 dias)'),
        ('BRONZE', 'Bronze (Individual)'),
        ('PRATA', 'Prata (Corretor)'),
        ('OURO', 'Ouro (Top Seller)'),
        ('IMOB_SMALL', 'Imobiliária Small'),
        ('IMOB_PRO', 'Imobiliária Pro'),
        ('IMOB_PREMIUM', 'Imobiliária Premium'),
    )
    
    nome = models.CharField(max_length=20, choices=NOME_CHOICES, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Limites
    max_imoveis = models.PositiveIntegerField(help_text="Quantidade máxima de imóveis ativos permitidos")
    max_fotos_por_imovel = models.PositiveIntegerField(default=20, help_text="O CEO pediu foco em qualidade visual")
    
    # Nova lógica de expiração pedida pelo CEO (em dias)
    dias_de_destaque = models.PositiveIntegerField(default=0, help_text="Quantos dias fica no topo?")
    dias_de_anuncio = models.PositiveIntegerField(default=90, help_text="Tempo antes do anúncio expirar")

    def __str__(self):
        return f"{self.get_nome_display()} - R$ {self.preco}"

class Anunciante(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anunciante_profile')
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)
    
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp/Telefone")
    creci = models.CharField(max_length=20, blank=True, help_text="Obrigatório para corretores")
    
    # Adicionei 'bairro_atuacao' para a estratégia da Zona Leste
    bairro_atuacao = models.CharField(max_length=100, blank=True, verbose_name="Bairro de Foco (Ex: Tatuapé)")
    bio = models.TextField(blank=True, verbose_name="Sobre o Anunciante")
    
    aprovado = models.BooleanField(default=False, verbose_name="Perfil Aprovado?")

    def __str__(self):
        return self.user.get_full_name() or self.user.username