from django.shortcuts import render, redirect, get_object_or_404
from .forms import EncomendaSurfForm
from .models import EncomendaSurf
from contratos.models import Pagamento
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from financeiro.models import MovimentacaoCaixa

@login_required
def encomenda_list(request):
    encomendas = EncomendaSurf.objects.all().order_by('-criado_em')
    return render(request, 'encomendas/encomenda_list.html', {'encomendas': encomendas})

@login_required
def encomenda_detail(request, pk):
    encomenda = get_object_or_404(EncomendaSurf, pk=pk)
    return render(request, 'encomendas/encomenda_detail.html', {'encomenda': encomenda})

@login_required
def encomenda_create(request):
    if request.method == 'POST':
        form = EncomendaSurfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('encomendas:encomenda_list')
    else:
        form = EncomendaSurfForm()
    
    return render(request, 'encomendas/form_encomenda.html', {'form': form, 'titulo': 'Nova Encomenda'})

@login_required
def encomenda_update(request, pk):
    encomenda = get_object_or_404(EncomendaSurf, pk=pk)
    if request.method == 'POST':
        form = EncomendaSurfForm(request.POST, request.FILES, instance=encomenda)
        if form.is_valid():
            form.save()
            return redirect('encomendas:encomenda_detail', pk=pk)
    else:
        form = EncomendaSurfForm(instance=encomenda)
    
    return render(request, 'encomendas/form_encomenda.html', {
        'form': form, 
        'titulo': 'Editar Encomenda',
        'encomenda': encomenda
    })

@login_required
def encomenda_fechar_pedido(request, pk):
    encomenda = get_object_or_404(EncomendaSurf, pk=pk)
    
    if encomenda.venda_lancada:
        messages.warning(request, "Esta venda já foi lançada no financeiro.")
        return redirect('encomendas:encomenda_detail', pk=pk)
    
    if not encomenda.valor_total or encomenda.valor_total <= 0:
        messages.error(request, "Informe o valor total da prancha antes de fechar o pedido.")
        return redirect('encomendas:encomenda_update', pk=pk)

    # 1. Registrar entrada no caixa (Valor de Entrada)
    if encomenda.valor_entrada and encomenda.valor_entrada > 0:
        MovimentacaoCaixa.objects.create(
            tipo='ENTRADA',
            categoria='PAGAMENTO_CLIENTE',
            tipo_receita='PRODUTO',
            valor=encomenda.valor_entrada,
            data=timezone.now().date(),
            descricao=f"Venda Prancha #{encomenda.id} - {encomenda.cliente.nome} (Entrada)"
        )

    # 2. Atualizar Encomenda
    encomenda.venda_lancada = True
    encomenda.status = 'PRODUCAO'
    encomenda.data_fechamento = timezone.now()
    encomenda.save()
    
    messages.success(request, f"Pedido #{encomenda.id} fechado com sucesso! Venda lançada no financeiro.")
    return redirect('encomendas:encomenda_detail', pk=pk)

@login_required
def registrar_pagamento_encomenda(request, pk):
    encomenda = get_object_or_404(EncomendaSurf, pk=pk)
    
    if request.method == 'POST':
        valor_raw = request.POST.get('valor')
        metodo = request.POST.get('metodo')
        data = request.POST.get('data') or timezone.now().date()
        
        if valor_raw:
            # Converte vírgula em ponto para garantir conversão decimal
            valor = valor_raw.replace(',', '.')
            Pagamento.objects.create(
                encomenda=encomenda,
                valor=valor,
                metodo=metodo,
                data_pagamento=data,
                observacao=f"Pagto Saldo Prancha #{encomenda.id}"
            )
            messages.success(request, f"Recebimento de R$ {valor} registrado com sucesso!")
        else:
            messages.error(request, "Informe o valor do pagamento.")
            
    return redirect('encomendas:encomenda_detail', pk=pk)

def render_form_step(request):
    tipo_prancha = request.GET.get('tipo_prancha')
    encomenda_id = request.GET.get('encomenda_id')
    
    instance = None
    if encomenda_id:
        instance = get_object_or_404(EncomendaSurf, pk=encomenda_id)
        
    form = EncomendaSurfForm(instance=instance)
    
    template_map = {
        'SHORTBOARD': 'encomendas/partials/fields_tecnicos.html',
        'FISH': 'encomendas/partials/fields_tecnicos.html',
        'LONGBOARD': 'encomendas/partials/fields_tecnicos.html',
        'FAN_BOARD': 'encomendas/partials/fields_tecnicos.html',
        'STAND_UP': 'encomendas/partials/fields_tecnicos.html',
    }
    
    template_name = template_map.get(tipo_prancha, 'encomendas/partials/empty.html')
    
    return render(request, template_name, {
        'form': form,
        'tipo_prancha': tipo_prancha,
        'encomenda': instance
    })
