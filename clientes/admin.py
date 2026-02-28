from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'documento', 'criado_em')
    search_fields = ('nome', 'email', 'documento')
    list_filter = ('criado_em',)

