from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contratos.models import Contrato
from financeiro.models import MovimentacaoCaixa
from encomendas.models import EncomendaSurf
from django.db.models import Sum, Q
from django.utils import timezone

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard:painel')
    return render(request, 'dashboard/landing.html')

@login_required(login_url='login')
def index(request):
    agora = timezone.now()
    
    # Resumo Financeiro (Fluxo de Caixa Real)
    total_entrada = MovimentacaoCaixa.objects.filter(tipo='ENTRADA').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saida = MovimentacaoCaixa.objects.filter(tipo='SAIDA').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_entrada - total_saida

    # Faturamento (KPI de Vendas - Valor total acordado)
    vendas_contratos = Contrato.objects.exclude(status='CANCELADO').aggregate(Sum('valor_final'))['valor_final__sum'] or 0
    vendas_encomendas = EncomendaSurf.objects.filter(venda_lancada=True).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    faturamento_total = vendas_contratos + vendas_encomendas

    # Agenda: Contratos (Eventos)
    proximos_eventos = Contrato.objects.filter(
        data_hora_evento__gte=agora,
        status__in=['ATIVO']
    ).order_by('data_hora_evento')[:5]

    # Agenda: Encomendas (Entregas Programadas)
    proximas_entregas = EncomendaSurf.objects.filter(
        data_previsao_entrega__gte=agora.date(),
        status__in=['FILA', 'PRODUCAO', 'FINALIZADA']
    ).order_by('data_previsao_entrega')[:5]
    
    # Controle de Recebíveis (Contratos)
    contratos_pendentes = Contrato.objects.filter(
        status_pagamento__in=['PENDENTE', 'PARCIAL'],
        status__in=['ATIVO', 'CONCLUIDO']
    ).order_by('-data_inicio')[:5]

    # Controle de Recebíveis (Encomendas)
    encomendas_pendentes = EncomendaSurf.objects.filter(
        venda_lancada=True,
        valor_restante__gt=0
    ).order_by('-criado_em')[:5]

    # Cálculo Total de Recebíveis
    receber_contratos = sum(c.saldo_restante for c in Contrato.objects.exclude(status='CANCELADO').exclude(status_pagamento='PAGO'))
    receber_encomendas = EncomendaSurf.objects.exclude(status='ENTREGUE').aggregate(Sum('valor_restante'))['valor_restante__sum'] or 0
    total_a_receber = receber_contratos + receber_encomendas

    context = {
        'saldo': saldo,
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'faturamento_total': faturamento_total,
        'total_a_receber': total_a_receber,
        'proximos_eventos': proximos_eventos,
        'proximas_entregas': proximas_entregas,
        'contratos_pendentes': contratos_pendentes,
        'encomendas_pendentes': encomendas_pendentes,
    }
    return render(request, 'dashboard/index.html', context)
