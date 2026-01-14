# imoveis/forms.py
from django import forms
from .models import Imovel

# --- 1. Widget que permite selecionar múltiplos arquivos no HTML ---
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# --- 2. Campo Personalizado que valida a lista de arquivos ---
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImovelForm(forms.ModelForm):
    # Usamos o nosso campo personalizado aqui
    imagens = MultipleFileField(
        label="Fotos do Imóvel (Selecione várias)",
        required=False
    )

    class Meta:
        model = Imovel
        exclude = ['anunciante', 'slug', 'status', 'views_count', 'data_criacao', 'data_atualizacao']
        
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.TextInput(attrs={'placeholder': 'Opcional (Preenchido auto se vazio)'}),
            'longitude': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Mantém o estilo Bootstrap/CSS
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
        # Adiciona o atributo multiple no widget de imagens
        self.fields['imagens'].widget.attrs.update({'multiple': True})