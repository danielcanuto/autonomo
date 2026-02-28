from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioCustomizado

class CustomUserAdmin(UserAdmin):
    model = UsuarioCustomizado
    list_display = ['username', 'email', 'first_name', 'last_name', 'cargo', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('cargo',)}),
    )

admin.site.register(UsuarioCustomizado, CustomUserAdmin)
