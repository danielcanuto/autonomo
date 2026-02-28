from django.db import models
from clientes.models import Cliente
from servicos.models import Servico

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

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contratos', verbose_name="Cliente")
    servicos = models.ManyToManyField(Servico, related_name='contratos', verbose_name="Serviços Contratados")
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Final (R$)")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de Término")
    data_hora_evento = models.DateTimeField(blank=True, null=True, verbose_name="Data e Hora do Evento")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status do Contrato")
    status_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES, default='PENDENTE', verbose_name="Status de Pagamento")
    termos = models.TextField(blank=True, null=True, verbose_name="Termos do Contrato")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return f"Contrato #{self.id} - {self.cliente.nome} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-data_inicio']

