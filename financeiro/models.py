from django.db import models
from django.utils import timezone
from contratos.models import Contrato

class Fornecedor(models.Model):
    CATEGORIA_CHOICES = (
        ('REVELACAO', 'Revelação de Fotos'),
        ('ALBUNS', 'Álbuns e Fotolivros'),
        ('CAIXAS', 'Caixas Personalizadas'),
        ('EQUIPAMENTO', 'Equipamentos e Manutenção'),
        ('TRANSPORTE', 'Transporte e Logística'),
        ('OUTROS', 'Outros'),
    )

    nome = models.CharField(max_length=100, verbose_name="Nome do Fornecedor")
    contato = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contato/Telefone")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='OUTROS', verbose_name="Categoria")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.get_categoria_display()})"

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

class Custo(models.Model):
    descricao = models.CharField(max_length=200, verbose_name="Descrição da Despesa")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    data = models.DateField(default=timezone.now, verbose_name="Data da Despesa")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='custos', verbose_name="Fornecedor")
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, blank=True, related_name='custos', verbose_name="Contrato Vinculado")
    pago = models.BooleanField(default=True, verbose_name="Status de Pagamento (Pago?)")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    class Meta:
        verbose_name = "Custo/Despesa"
        verbose_name_plural = "Custos e Despesas"
        ordering = ['-data']

class MovimentacaoCaixa(models.Model):
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada (+)'),
        ('SAIDA', 'Saída (-)'),
    )
    CATEGORIA_CAIXA = (
        ('PAGAMENTO_CLIENTE', 'Recebimento de Contrato'),
        ('PAGAMENTO_FORNECEDOR', 'Pagamento de Fornecedor'),
        ('TRANSPORTE', 'Transporte/Combustível'),
        ('MARKETING', 'Marketing e Divulgação'),
        ('ALUGUEL', 'Aluguel/Estúdio'),
        ('DIVERSOS', 'Diversos'),
    )

    TIPO_RECEITA_CHOICES = (
        ('SERVICO', 'Prestação de Serviços'),
        ('PRODUTO', 'Revenda de Mercadorias'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CAIXA, default='DIVERSOS', verbose_name="Categoria")
    tipo_receita = models.CharField(max_length=10, choices=TIPO_RECEITA_CHOICES, default='SERVICO', verbose_name="Tipo de Receita (MEI)", blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    data = models.DateField(default=timezone.now, verbose_name="Data")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    
    # Links opcionais
    custo_ref = models.OneToOneField(Custo, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacao', verbose_name="Referência de Custo")
    
    def __str__(self):
        simbolo = "+" if self.tipo == 'ENTRADA' else "-"
        return f"{simbolo} R$ {self.valor} - {self.descricao}"

    class Meta:
        verbose_name = "Movimentação de Caixa"
        verbose_name_plural = "Fluxo de Caixa"
        ordering = ['-data', '-id']

# Sinais para automação
from django.db.models.signals import post_save
from django.dispatch import receiver
from contratos.models import Pagamento

@receiver(post_save, sender=Pagamento)
def criar_movimentacao_pagamento(sender, instance, created, **kwargs):
    if created:
        if instance.contrato:
            descricao = f"Recbto: {instance.contrato.cliente.nome} ({instance.get_metodo_display()})"
        elif instance.orcamento:
            descricao = f"Sinal/Reserva: {instance.orcamento.cliente.nome} ({instance.get_metodo_display()})"
        elif instance.encomenda:
            descricao = f"Pactuado: {instance.encomenda.cliente.nome} (Prancha #{instance.encomenda.id})"
        else:
            descricao = f"Recebimento Avulso ({instance.get_metodo_display()})"

        MovimentacaoCaixa.objects.create(
            tipo='ENTRADA',
            categoria='PAGAMENTO_CLIENTE',
            valor=instance.valor,
            data=instance.data_pagamento,
            descricao=descricao,
        )
