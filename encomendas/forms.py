from django import forms
from .models import EncomendaSurf

class EncomendaSurfForm(forms.ModelForm):
    class Meta:
        model = EncomendaSurf
        exclude = ['criado_em']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'tipo_prancha': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'peso': forms.TextInput(attrs={'placeholder': 'Ex: 75kg', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'altura': forms.TextInput(attrs={'placeholder': 'Ex: 1.80m', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'tamanho': forms.TextInput(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'quilhas': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'tipo_fundo': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'rabeta': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'bordas': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'tipo_laminacao': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'copinho': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'pintura_desejada': forms.CheckboxInput(attrs={'class': 'rounded text-indigo-600 focus:ring-indigo-500 h-5 w-5'}),
            'tipo_pintura': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'quantidade_cores': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'link_imagem_pintura': forms.URLInput(attrs={'placeholder': 'https://...', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'pintura_arquivo': forms.ClearableFileInput(attrs={'class': 'w-full text-xs text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-black file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'shape_3d_arquivo': forms.ClearableFileInput(attrs={'class': 'w-full text-xs text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-black file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'modelo_especifico': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'status': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'data_encomenda': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'data_previsao_entrega': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
            'valor_total': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0,00', 'class': 'w-full rounded-lg border-gray-300 shadow-sm font-bold text-indigo-600'}),
            'valor_entrada': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0,00', 'class': 'w-full rounded-lg border-gray-300 shadow-sm'}),
        }
