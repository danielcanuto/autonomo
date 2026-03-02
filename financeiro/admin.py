from django.contrib import admin
from .models import Fornecedor, Custo, MovimentacaoCaixa

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'contato', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)

@admin.register(Custo)
class CustoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'fornecedor', 'contrato', 'pago')
    list_filter = ('data', 'pago', 'fornecedor')
    search_fields = ('descricao',)

@admin.register(MovimentacaoCaixa)
class MovimentacaoCaixaAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipo', 'categoria', 'valor', 'descricao')
    list_filter = ('tipo', 'categoria', 'data')
    search_fields = ('descricao',)
