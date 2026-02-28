from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'valor_final', 'data_inicio', 'data_hora_evento', 'status', 'status_pagamento')
    list_filter = ('status', 'status_pagamento', 'data_inicio', 'data_hora_evento')
    search_fields = ('cliente__nome',)
    filter_horizontal = ('servicos',)

