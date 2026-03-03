from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from servicos.models import Servico
from orcamentos.models import Orcamento
# Removido import direto para evitar circularidade
# from encomendas.models import EncomendaSurf

class Contrato(models.Model):
    STATUS_CHOICES = (
        ('RASCUNHO', 'Rascunho'),
        ('ATIVO', 'Ativo'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    )

    PAGAMENTO_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PARCIAL', 'Parcial'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    )

    CONDICAO_CHOICES = (
        ('A_VISTA', 'À Vista'),
        ('PARCELADO', 'Parcelado'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('CARTAO', 'Cartão'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contratos', verbose_name="Cliente")
    servicos = models.ManyToManyField(Servico, related_name='contratos', verbose_name="Serviços Contratados")
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Bruto (R$)")
    tipo_desconto = models.CharField(
        max_length=20, 
        choices=(('VALOR', 'R$'), ('PERCENTUAL', '%')), 
        default='VALOR', 
        verbose_name="Tipo de Desconto"
    )
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Final Acordado (R$)")
    data_inicio = models.DateField(verbose_name="Data do Contrato")
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de Término")
    data_hora_evento = models.DateTimeField(blank=True, null=True, verbose_name="Data e Hora do Evento")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status do Contrato")
    status_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES, default='PENDENTE', verbose_name="Condição de Pagamento")
    condicao_pagamento = models.CharField(max_length=20, choices=CONDICAO_CHOICES, default='A_VISTA', verbose_name="Forma de Pagamento")
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor de Entrada (R$)")
    arquivo_contrato = models.FileField(upload_to='contratos/assinados/', blank=True, null=True, verbose_name="Contrato Assinado")
    termos = models.TextField(blank=True, null=True, verbose_name="Termos do Contrato")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    @property
    def valor_pago(self):
        pagamentos_extras = self.pagamentos.aggregate(models.Sum('valor'))['valor__sum'] or 0
        return self.valor_entrada + pagamentos_extras

    @property
    def saldo_restante(self):
        return self.valor_final - self.valor_pago

    @property
    def total_servicos(self):
        return sum(s.preco_base for s in self.servicos.all())

    def __str__(self):
        return f"Contrato #{self.id} - {self.cliente.nome} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-data_inicio']


class Pagamento(models.Model):
    METODO_CHOICES = (
        ('PIX', 'PIX'),
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('TRANSFERENCIA', 'Transferência'),
    )

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='pagamentos', verbose_name="Contrato", null=True, blank=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='pagamentos', verbose_name="Orçamento", null=True, blank=True)
    encomenda = models.ForeignKey('encomendas.EncomendaSurf', on_delete=models.CASCADE, related_name='pagamentos', verbose_name="Encomenda", null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago (R$)")
    data_pagamento = models.DateField(default=timezone.now, verbose_name="Data do Pagamento")
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default='PIX', verbose_name="Método de Pagamento")
    observacao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Observação")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        cliente = "Desconhecido"
        if self.contrato: cliente = self.contrato.cliente.nome
        elif self.orcamento: cliente = self.orcamento.cliente.nome
        elif self.encomenda: cliente = self.encomenda.cliente.nome
        return f"Pagamento R$ {self.valor} - {cliente}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_pagamento']


# Sinais para atualização de saldos
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Pagamento)
def atualizar_saldo_encomenda(sender, instance, **kwargs):
    if instance.encomenda:
        instance.encomenda.save() # O save da encomenda já recalcula o valor_restante

