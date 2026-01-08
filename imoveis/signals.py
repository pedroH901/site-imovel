# imoveis/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from PIL import Image
import os
from .models import ImovelImagem

@receiver(post_save, sender=ImovelImagem)
def otimizar_imagem(sender, instance, created, **kwargs):
    """
    Redimensiona a imagem logo após o upload para economizar espaço e banda.
    """
    if created and instance.imagem: # Só processa se for uma imagem nova
        try:
            caminho_imagem = instance.imagem.path
            
            # Abre a imagem
            img = Image.open(caminho_imagem)
            
            # Define largura máxima (Full HD é um bom padrão pra web)
            max_width = 1920 
            
            if img.width > max_width:
                # Calcula a altura proporcional
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * float(ratio))
                
                # Redimensiona com filtro de alta qualidade
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Salva otimizando
                img.save(caminho_imagem, quality=85, optimize=True)
                
        except Exception as e:
            print(f"Erro ao otimizar imagem: {e}")

@receiver(pre_delete, sender=ImovelImagem)
def deletar_arquivo_fisico(sender, instance, **kwargs):
    """
    Remove o arquivo da pasta media quando o registro é deletado do banco.
    Evita ficar com lixo no servidor.
    """
    if instance.imagem:
        if os.path.isfile(instance.imagem.path):
            os.remove(instance.imagem.path)