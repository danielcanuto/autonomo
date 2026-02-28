from django.db import models

class Cliente(models.Model):

    nome = models.CharField(max_length=255, verbose_name="Nome Completo / Razão Social")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço Completo")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

