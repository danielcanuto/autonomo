from django.contrib import admin
from .models import Categoria, Servico

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_base', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)

