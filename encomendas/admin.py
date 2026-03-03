from django.contrib import admin
from .models import EncomendaSurf

@admin.register(EncomendaSurf)
class EncomendaSurfAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo_prancha', 'tamanho', 'criado_em')
    list_filter = ('tipo_prancha', 'quilhas', 'rabeta', 'pintura_desejada')
    search_fields = ('cliente__nome', 'tamanho')
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cliente', 'contrato', 'tipo_prancha')
        }),
        ('Medidas do Simétrico', {
            'fields': ('peso', 'altura', 'tamanho', 'modelo_especifico')
        }),
        ('Configurações Técnicas', {
            'fields': ('quilhas', 'tipo_fundo', 'rabeta', 'copinho')
        }),
        ('Laminação e Acabamento', {
            'fields': ('bordas', 'tipo_laminacao')
        }),
        ('Design e Estética', {
            'fields': ('pintura_desejada', 'tipo_pintura', 'quantidade_cores', 'link_imagem_pintura')
        }),
    )
