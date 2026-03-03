from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contratos.models import Contrato
from financeiro.models import MovimentacaoCaixa
from django.db.models import Sum
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
    from encomendas.models import EncomendaSurf
    vendas_contratos = Contrato.objects.exclude(status='CANCELADO').aggregate(Sum('valor_final'))['valor_final__sum'] or 0
    vendas_encomendas = EncomendaSurf.objects.filter(venda_lancada=True).aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    faturamento_total = vendas_contratos + vendas_encomendas

    # Próximos Eventos
    proximos_eventos = Contrato.objects.filter(
        data_hora_evento__gte=agora,
        status__in=['ATIVO']
    ).order_by('data_hora_evento')[:5]
    
    # Contratos com pagamentos pendentes
    pagamentos_pendentes = Contrato.objects.filter(
        status_pagamento__in=['PENDENTE', 'PARCIAL'],
        status__in=['ATIVO', 'CONCLUIDO']
    ).order_by('-data_inicio')[:5]

    context = {
        'saldo': saldo,
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'faturamento_total': faturamento_total,
        'proximos_eventos': proximos_eventos,
        'pagamentos_pendentes': pagamentos_pendentes,
    }
    return render(request, 'dashboard/index.html', context)
