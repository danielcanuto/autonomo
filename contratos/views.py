from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contrato, Pagamento
from .forms import ContratoForm, PagamentoForm
from servicos.models import Servico
from django.contrib import messages

@login_required(login_url='login')
def contrato_list(request):
    contratos = Contrato.objects.all().select_related('cliente').prefetch_related('servicos')
    return render(request, 'contratos/contrato_list.html', {'contratos': contratos})

@login_required(login_url='login')
def contrato_create(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Contrato criado com sucesso!")
            return redirect('contratos:contrato_list')
        else:
            messages.error(request, "Erro ao salvar contrato. Verifique os campos abaixo.")
    else:
        form = ContratoForm()
    
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'contratos/contrato_form.html', {
        'form': form, 
        'titulo': 'Novo Contrato',
        'all_servicos': servicos
    })

@login_required(login_url='login')
def contrato_update(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES, instance=contrato)
        if form.is_valid():
            form.save()
            messages.success(request, "Contrato atualizado com sucesso!")
            return redirect('contratos:contrato_list')
        else:
            messages.error(request, "Erro ao atualizar contrato. Verifique os campos abaixo.")
    else:
        form = ContratoForm(instance=contrato)
    
    pagamento_form = PagamentoForm()
    historico_pagamentos = contrato.pagamentos.all()
    servicos = Servico.objects.filter(ativo=True)
    
    return render(request, 'contratos/contrato_form.html', {
        'form': form, 
        'pagamento_form': pagamento_form,
        'historico_pagamentos': historico_pagamentos,
        'contrato': contrato,
        'titulo': 'Editar Contrato',
        'all_servicos': servicos
    })

@login_required(login_url='login')
def registrar_pagamento(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.contrato = contrato
            pagamento.save()
            
            # Auto-update contract payment status if fully paid
            if contrato.saldo_restante <= 0:
                contrato.status_pagamento = 'PAGO'
                contrato.save()
            elif contrato.valor_pago > 0:
                contrato.status_pagamento = 'PARCIAL'
                contrato.save()
                
    return redirect('contratos:contrato_update', pk=pk)
@login_required(login_url='login')
def finalizar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        contrato.status = 'CONCLUIDO'
        contrato.save()
    return redirect('contratos:contrato_update', pk=pk)
