# imoveis/models.py
from django.db import models
from django.utils.text import slugify
from accounts.models import Anunciante
from core.models import TimeStampedModel

class Imovel(TimeStampedModel):
    # Enums baseados no HTML para facilitar a busca
    TIPO_CHOICES = (
        ('CASA', 'Casa'),
        ('APARTAMENTO', 'Apartamento'),
        ('COBERTURA', 'Cobertura'),
        ('TERRENO', 'Terreno'),
        ('COMERCIAL', 'Comercial'),
        ('RURAL', 'Rural'),
    ) #
    
    TRANSACAO_CHOICES = (
        ('VENDA', 'Venda'),
        ('ALUGUEL', 'Aluguel'),
    ) #

    STATUS_CHOICES = (
        ('RASCUNHO', 'Rascunho'),
        ('PENDENTE', 'Aguardando Aprovação'), # Fluxo de aprovação (Fase 4)
        ('ATIVO', 'Ativo'),
        ('VENDIDO', 'Vendido/Alugado'),
    )

    # Relacionamento
    anunciante = models.ForeignKey(Anunciante, on_delete=models.CASCADE, related_name='imoveis')

    # Dados Principais
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField()
    
    # Características Físicas (Baseado nos cards do HTML)
    tipo_imovel = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_transacao = models.CharField(max_length=20, choices=TRANSACAO_CHOICES)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    
    quartos = models.PositiveIntegerField(default=0) #
    banheiros = models.PositiveIntegerField(default=0) #
    vagas_garagem = models.PositiveIntegerField(default=0)
    area_total = models.PositiveIntegerField(help_text="Em m²") #
    
    # Localização
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    bairro = models.CharField(max_length=100) # Importante para filtro
    cidade = models.CharField(max_length=100) # Importante para filtro
    estado = models.CharField(max_length=2)
    
    # Status de Sistema
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    destaque = models.BooleanField(default=False, help_text="Exibir na home como destaque?")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Cria slug único: "apartamento-jardins-sp-id123"
            self.slug = slugify(f"{self.tipo_imovel}-{self.bairro}-{self.cidade}") + f"-{self.pk}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'tipo_transacao', 'cidade']), # Otimiza busca
        ]

class ImovelImagem(TimeStampedModel):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='imoveis/%Y/%m/')
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"Imagem de {self.imovel.titulo}"

class Lead(TimeStampedModel):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='leads')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField(blank=True)
    
    # Controle
    respondido = models.BooleanField(default=False)

    def __str__(self):
        return f"Lead de {self.nome} para {self.imovel.titulo}"