from django.contrib import admin
from .models import Contrato, Pagamento

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'valor_final', 'data_inicio', 'status', 'status_pagamento')
    list_filter = ('status', 'status_pagamento', 'data_inicio')
    search_fields = ('cliente__nome',)
    filter_horizontal = ('servicos',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'valor', 'data_pagamento', 'metodo')
    list_filter = ('metodo', 'data_pagamento')
    search_fields = ('contrato__cliente__nome',)

