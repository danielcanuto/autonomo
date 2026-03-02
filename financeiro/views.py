from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Fornecedor, Custo, MovimentacaoCaixa
from contratos.models import Contrato, Pagamento
from django.db import models
from django.db.models import Sum

@login_required
def financeiro_dashboard(request):
    movimentacoes = MovimentacaoCaixa.objects.all()[:10]
    total_entrada = MovimentacaoCaixa.objects.filter(tipo='ENTRADA').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saida = MovimentacaoCaixa.objects.filter(tipo='SAIDA').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_entrada - total_saida
    
    return render(request, 'financeiro/dashboard.html', {
        'movimentacoes': movimentacoes,
        'saldo': saldo,
        'total_entrada': total_entrada,
        'total_saida': total_saida,
    })

# Fornecedores
@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'financeiro/fornecedor_list.html', {'fornecedores': fornecedores})

@login_required
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financeiro:fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'financeiro/fornecedor_form.html', {'form': form, 'titulo': 'Novo Fornecedor'})

@login_required
def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('financeiro:fornecedor_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'financeiro/fornecedor_form.html', {'form': form, 'titulo': 'Editar Fornecedor'})

@login_required
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('financeiro:fornecedor_list')
    return render(request, 'financeiro/confirm_delete.html', {'objeto': fornecedor, 'voltar': 'financeiro:fornecedor_list'})

# Custos
@login_required
def custo_list(request):
    custos = Custo.objects.all().select_related('fornecedor', 'contrato')
    return render(request, 'financeiro/custo_list.html', {'custos': custos})

@login_required
def custo_create(request):
    if request.method == 'POST':
        form = CustoForm(request.POST)
        if form.is_valid():
            custo = form.save()
            # Se já está pago, gera movimentação automática
            if custo.pago:
                MovimentacaoCaixa.objects.create(
                    tipo='SAIDA',
                    categoria='PAGAMENTO_FORNECEDOR',
                    valor=custo.valor,
                    data=custo.data,
                    descricao=f"Pagto: {custo.descricao}",
                    custo_ref=custo
                )
            return redirect('financeiro:custo_list')
    else:
        form = CustoForm()
    return render(request, 'financeiro/custo_form.html', {'form': form, 'titulo': 'Novo Custo/Despesa'})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def sync_financeiro(request):
    # Limpa movimentações automáticas para evitar duplicados
    # MovimentacaoCaixa.objects.filter(categoria__in=['PAGAMENTO_CLIENTE', 'PAGAMENTO_FORNECEDOR']).delete()
    
    # Sincroniza Entradas (Pagamentos Registrados)
    for pgto in Pagamento.objects.all():
        if pgto.contrato:
            descricao = f"Recbto: {pgto.contrato.cliente.nome} ({pgto.get_metodo_display()})"
        elif pgto.orcamento:
            descricao = f"Sinal/Reserva: {pgto.orcamento.cliente.nome} ({pgto.get_metodo_display()})"
        else:
            descricao = f"Recebimento Avulso ({pgto.get_metodo_display()})"

        MovimentacaoCaixa.objects.get_or_create(
            descricao=descricao,
            valor=pgto.valor,
            data=pgto.data_pagamento,
            tipo='ENTRADA',
            categoria='PAGAMENTO_CLIENTE'
        )
    
    # Sincroniza Contratos Antigos (que não tinham a tabela de Pagamentos mas estão como PAGO)
    # Isso garante que o saldo não fique zerado se houver contratos finalizados
    for contrato in Contrato.objects.filter(status_pagamento='PAGO'):
        # Verifica se já não tem pagamento registrado para evitar duplicidade
        if not Pagamento.objects.filter(contrato=contrato).exists():
            MovimentacaoCaixa.objects.get_or_create(
                descricao=f"Contrato Antigo: {contrato.cliente.nome} (Sincronizado)",
                valor=contrato.valor_final,
                data=contrato.data_inicio,
                tipo='ENTRADA',
                categoria='PAGAMENTO_CLIENTE'
            )
        
    # Sincroniza Saídas (Custos Pagos)
    for custo in Custo.objects.filter(pago=True):
        MovimentacaoCaixa.objects.get_or_create(
            descricao=f"Pagto: {custo.descricao}",
            valor=custo.valor,
            data=custo.data,
            tipo='SAIDA',
            categoria='PAGAMENTO_FORNECEDOR',
            custo_ref=custo
        )
        
    return redirect('financeiro:dashboard')

@login_required
def relatorio_mei(request):
    from django.db.models.functions import ExtractMonth, ExtractYear
    import datetime

    # Filtra apenas entradas (receitas)
    entradas = MovimentacaoCaixa.objects.filter(tipo='ENTRADA')
    
    # Agrupa por Ano e Mês
    dados = entradas.annotate(
        mes=ExtractMonth('data'),
        ano=ExtractYear('data')
    ).values('ano', 'mes').annotate(
        total_servico=Sum('valor', filter=models.Q(tipo_receita='SERVICO')),
        total_produto=Sum('valor', filter=models.Q(tipo_receita='PRODUTO'))
    ).order_by('-ano', '-mes')

    # Adiciona nome do mês por extenso
    meses_nome = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    for d in dados:
        d['nome_mes'] = meses_nome.get(d['mes'])
        d['total_geral'] = (d['total_servico'] or 0) + (d['total_produto'] or 0)

    return render(request, 'financeiro/report_mei.html', {'dados_mensais': dados})
