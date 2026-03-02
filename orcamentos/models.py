from django.db import models
from clientes.models import Cliente
from servicos.models import Servico

class Orcamento(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
        ('EXPIRADO', 'Expirado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos', verbose_name="Cliente")
    servicos = models.ManyToManyField(Servico, related_name='orcamentos', verbose_name="Serviços")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total (R$)")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data de Criação")
    data_validade = models.DateField(blank=True, null=True, verbose_name="Validade")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome} ({self.status})"

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ['-data_criacao']
