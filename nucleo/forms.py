from django import forms
from .models import UsuarioCustomizado

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Senha (deixe em branco para não alterar)")

    class Meta:
        model = UsuarioCustomizado
        fields = ['first_name', 'last_name', 'email', 'cargo', 'is_active']
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'cargo': 'Perfil/Cargo',
            'is_active': 'Ativo'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome_fantasia', 'razao_social', 'cnpj_cpf', 'logo', 'endereco', 'telefone', 'email', 'inscricao_estadual']
        widgets = {
            'nome_fantasia': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'razao_social': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'cnpj_cpf': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'CNPJ ou CPF'}),
            'endereco': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'telefone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        }
