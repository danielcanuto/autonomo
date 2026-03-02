from django.contrib import admin
from .models import Orcamento

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor_total', 'data_criacao', 'data_validade', 'status')
    list_filter = ('status', 'data_criacao')
    search_fields = ('cliente__nome', 'observacoes')
    filter_horizontal = ('servicos',)
