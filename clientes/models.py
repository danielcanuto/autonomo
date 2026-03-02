from django.db import models
import re

class Cliente(models.Model):
    TIPO_PESSOA_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    nome = models.CharField(max_length=255, verbose_name="Nome Completo / Razão Social")
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA_CHOICES, default='PF', verbose_name="Tipo de Pessoa")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ", unique=True)
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço Completo")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    @property
    def telefone_formatado(self):
        if not self.telefone:
            return ""
        t = re.sub(r'\D', '', self.telefone)
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        elif len(t) == 10:
            return f"({t[:2]}) {t[2:6]}-{t[6:]}"
        return self.telefone

    @property
    def documento_formatado(self):
        if not self.documento:
            return ""
        d = self.documento
        if self.tipo_pessoa == 'PF' and len(d) == 11:
            return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"
        elif self.tipo_pessoa == 'PJ' and len(d) == 14:
            return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"
        return d

    def categorias_servicos(self):
        """Retorna as categorias únicas de serviços contratados (via contratos ou orçamentos)"""
        from servicos.models import Categoria
        from contratos.models import Contrato
        from orcamentos.models import Orcamento

        # Categorias de Contratos
        cats_contratos = Categoria.objects.filter(
            servicos__contratos__cliente=self
        ).distinct()

        # Categorias de Orçamentos
        cats_orcamentos = Categoria.objects.filter(
            servicos__orcamentos__cliente=self
        ).distinct()

        # União e retorno único
        return (cats_contratos | cats_orcamentos).distinct()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

