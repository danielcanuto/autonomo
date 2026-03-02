from django import forms
from .models import Categoria, Servico

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Ex: Fotografia, Consultoria'}),
            'descricao': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 2, 'placeholder': 'Breve descrição da categoria'}),
        }

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['categoria', 'nome', 'preco_base', 'descricao', 'ativo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'nome': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Nome do serviço'}),
            'preco_base': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': '0.00', 'step': '0.01'}),
            'descricao': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 3, 'placeholder': 'O que está incluído no serviço?'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'}),
        }
