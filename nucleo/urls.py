from django.urls import path
from . import views

app_name = 'nucleo'

urlpatterns = [
    path('equipe/', views.equipe_list, name='equipe_list'),
    path('equipe/novo/', views.usuario_create, name='usuario_create'),
    path('equipe/editar/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('configuracao/', views.configuracao_empresa, name='empresa_configuracao'),
]
