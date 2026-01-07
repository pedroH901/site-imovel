# accounts/models.py
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel # Importe da classe base acima

class Plano(TimeStampedModel):
    NOME_CHOICES = (
        ('GRATIS', 'Gratuito'),
        ('PREMIUM', 'Premium'),
    )
    nome = models.CharField(max_length=20, choices=NOME_CHOICES, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_imoveis = models.PositiveIntegerField(help_text="Quantidade máxima de imóveis ativos permitidos")
    max_fotos_por_imovel = models.PositiveIntegerField(default=5)
    
    def __str__(self):
        return f"{self.get_nome_display()} - R$ {self.preco}"

class Anunciante(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anunciante_profile')
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp/Telefone")
    creci = models.CharField(max_length=20, blank=True, help_text="Obrigatório para corretores")
    bio = models.TextField(blank=True, verbose_name="Sobre o Anunciante")
    
    # Controle de aprovação do Admin (Fase 4 do roadmap, mas já estruturamos aqui)
    aprovado = models.BooleanField(default=False, verbose_name="Perfil Aprovado?")

    def __str__(self):
        return self.user.get_full_name() or self.user.username