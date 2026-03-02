from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UsuarioCustomizado
from .forms import UsuarioForm

def gestor_check(user):
    return user.is_gestor_plus

@login_required
@user_passes_test(gestor_check)
def equipe_list(request):
    colaboradores = UsuarioCustomizado.objects.all().order_by('cargo', 'first_name')
    return render(request, 'nucleo/equipe_list.html', {'colaboradores': colaboradores})

@login_required
@user_passes_test(gestor_check)
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # For new users, enforce a username if not provided (e.g., use email)
            user = form.save(commit=False)
            if not user.username:
                user.username = user.email
            user.save()
            return redirect('nucleo:equipe_list')
    else:
        form = UsuarioForm()
    return render(request, 'nucleo/usuario_form.html', {'form': form, 'titulo': 'Novo Colaborador'})

@login_required
@user_passes_test(gestor_check)
def usuario_update(request, pk):
    usuario = get_object_or_404(UsuarioCustomizado, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('nucleo:equipe_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'nucleo/usuario_form.html', {'form': form, 'titulo': 'Editar Colaborador'})

from .models import Empresa
from .forms import EmpresaForm

@login_required
@user_passes_test(lambda u: u.is_gestor_plus)
def configuracao_empresa(request):
    empresa = Empresa.objects.first()
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('dashboard:painel')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'nucleo/empresa_form.html', {'form': form, 'titulo': 'Configurações da Empresa'})
