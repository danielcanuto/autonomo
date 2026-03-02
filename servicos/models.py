from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']


class Servico(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicos', verbose_name="Categoria")
    nome = models.CharField(max_length=200, verbose_name="Nome do Serviço")
    preco_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Base (R$)")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Detalhada")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    template_texto = models.TextField(blank=True, null=True, verbose_name="Texto Base para Orçamento", help_text="Use variáveis como {{cliente}}, {{valor}}, {{data}} para personalizar.")

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_base}"

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['nome']

