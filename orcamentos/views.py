from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Orcamento
from .forms import OrcamentoForm
from contratos.models import Contrato, Pagamento
from servicos.models import Servico
from django.utils import timezone

@login_required
def orcamento_list(request):
    orcamentos = Orcamento.objects.all().select_related('cliente')
    return render(request, 'orcamentos/orcamento_list.html', {'orcamentos': orcamentos})

@login_required
def orcamento_detail(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    return render(request, 'orcamentos/orcamento_detail.html', {'orcamento': orcamento})

@login_required
def orcamento_create(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orcamentos:orcamento_list')
    else:
        form = OrcamentoForm()
    
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'orcamentos/orcamento_form.html', {
        'form': form, 
        'titulo': 'Novo Orçamento',
        'all_servicos': servicos
    })

@login_required
def orcamento_update(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            return redirect('orcamentos:orcamento_list')
    else:
        form = OrcamentoForm(instance=orcamento)
    
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'orcamentos/orcamento_form.html', {
        'form': form, 
        'titulo': 'Editar Orçamento',
        'all_servicos': servicos
    })

@login_required
def converter_em_contrato(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        # Create a new Contract from the Budget
        contrato = Contrato.objects.create(
            cliente=orcamento.cliente,
            valor_final=orcamento.valor_total,
            data_inicio=timezone.now().date(),
            status='ATIVO' # Já ativa o contrato ao converter
        )
        contrato.servicos.set(orcamento.servicos.all())
        
        # Transferir pagamentos já realizados de Orçamento para o novo Contrato
        orcamento.pagamentos.update(contrato=contrato)
        
        # Registrar novo pagamento (Sinal) se fornecido na tela de confirmação
        valor_sinal_str = request.POST.get('valor_sinal')
        metodo = request.POST.get('metodo_pagamento')
        
        if valor_sinal_str:
            try:
                from decimal import Decimal
                valor_sinal = Decimal(valor_sinal_str.replace(',', '.'))
                if valor_sinal > 0:
                    Pagamento.objects.create(
                        contrato=contrato,
                        orcamento=orcamento, # Mantém vínculo com ambos para histórico
                        valor=valor_sinal,
                        data_pagamento=timezone.now().date(),
                        metodo=metodo or 'OUTRO',
                        observacao="Sinal/Pagamento inicial gerado na conversão do orçamento."
                    )
            except (ValueError, TypeError, NameError):
                pass
        
        # Atualizar status de pagamento do contrato baseado no total pago
        total_pago = contrato.valor_pago
        if total_pago >= contrato.valor_final:
            contrato.status_pagamento = 'PAGO'
        elif total_pago > 0:
            contrato.status_pagamento = 'PARCIAL'
        else:
            contrato.status_pagamento = 'PENDENTE'
        
        contrato.save()

        orcamento.status = 'APROVADO'
        orcamento.save()
        return redirect('contratos:contrato_update', pk=contrato.pk)
    return render(request, 'orcamentos/converter_confirm.html', {'orcamento': orcamento})

@login_required
def orcamento_pagamento_create(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        valor = request.POST.get('valor')
        metodo = request.POST.get('metodo')
        data = request.POST.get('data') or timezone.now().date()
        
        if valor:
            try:
                from decimal import Decimal
                valor_decimal = Decimal(valor.replace(',', '.'))
                Pagamento.objects.create(
                    orcamento=orcamento,
                    valor=valor_decimal,
                    data_pagamento=data,
                    metodo=metodo,
                    observacao=f"Sinal registrado no Orçamento #{orcamento.id}"
                )
            except (ValueError, TypeError):
                pass
    return redirect('orcamentos:orcamento_update', pk=pk)
