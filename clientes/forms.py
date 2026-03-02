from django import forms
from .models import Cliente
from validate_docbr import CPF, CNPJ
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'tipo_pessoa', 'email', 'telefone', 'documento', 'endereco', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Nome completo ou Razão Social'}),
            'tipo_pessoa': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'onchange': 'toggleDocumentLabel(this.value)'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': '(00) 00000-0000'}),
            'documento': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': '000.000.000-00'}),
            'endereco': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 3, 'placeholder': 'Rua, Número, Bairro, Cidade...'}),
            'observacoes': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 3, 'placeholder': 'Notas adicionais sobre o cliente'}),
        }

    def clean_documento(self):
        doc = self.cleaned_data.get('documento')
        tipo = self.cleaned_data.get('tipo_pessoa')
        
        # Remove caracteres não numéricos
        doc_limpo = re.sub(r'\D', '', doc)
        
        if tipo == 'PF':
            if not CPF().validate(doc_limpo):
                raise forms.ValidationError("CPF inválido.")
        elif tipo == 'PJ':
            if not CNPJ().validate(doc_limpo):
                raise forms.ValidationError("CNPJ inválido.")
        
        return doc_limpo
