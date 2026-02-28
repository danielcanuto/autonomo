from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioCustomizado(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('AUXILIAR', 'Auxiliar'),
    )
    cargo = models.CharField(max_length=20, choices=ROLE_CHOICES, default='AUXILIAR', verbose_name="Perfil/Cargo")

