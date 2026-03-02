from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categoria, Servico
from .forms import CategoriaForm, ServicoForm

@login_required(login_url='login')
def servico_list(request):
    servicos = Servico.objects.all().select_related('categoria')
    categorias = Categoria.objects.all()
    return render(request, 'servicos/servico_list.html', {
        'servicos': servicos,
        'categorias': categorias
    })

@login_required(login_url='login')
def servico_create(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicos:servico_list')
    else:
        form = ServicoForm()
    return render(request, 'servicos/servico_form.html', {'form': form, 'titulo': 'Novo Serviço'})

@login_required(login_url='login')
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicos:servico_list')
    else:
        form = CategoriaForm()
    return render(request, 'servicos/categoria_form.html', {'form': form, 'titulo': 'Nova Categoria'})
