from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioCustomizado(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador de Sistema'),
        ('GESTOR', 'Gestor'),
        ('VENDEDOR', 'Vendedor'),
        ('OPERADOR', 'Operador (Executor)'),
    )
    cargo = models.CharField(max_length=20, choices=ROLE_CHOICES, default='GESTOR', verbose_name="Perfil/Cargo")

    @property
    def is_admin(self):
        return self.cargo == 'ADMIN' or self.is_superuser

    @property
    def is_gestor_plus(self):
        return self.cargo in ['ADMIN', 'GESTOR'] or self.is_superuser

    @property
    def is_vendedor_plus(self):
        return self.cargo in ['ADMIN', 'GESTOR', 'VENDEDOR'] or self.is_superuser

class Empresa(models.Model):
    razao_social = models.CharField(max_length=200, verbose_name="Razão Social / Nome Completo")
    nome_fantasia = models.CharField(max_length=200, verbose_name="Nome Fantasia / Marca")
    cnpj_cpf = models.CharField(max_length=20, verbose_name="CNPJ ou CPF", blank=True, null=True)
    logo = models.ImageField(upload_to='empresa/', blank=True, null=True, verbose_name="Logo da Empresa")
    
    # Endereço
    endereco = models.CharField(max_length=255, verbose_name="Endereço Completo", blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone de Contato", blank=True, null=True)
    email = models.EmailField(verbose_name="E-mail de Contato", blank=True, null=True)
    
    # Documentação
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True, verbose_name="Inscrição Estadual")
    
    def __str__(self):
        return self.nome_fantasia

    class Meta:
        verbose_name = "Dados da Empresa"
        verbose_name_plural = "Dados da Empresa"

