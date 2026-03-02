from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('', views.financeiro_dashboard, name='dashboard'),
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/editar/<int:pk>/', views.fornecedor_update, name='fornecedor_update'),
    path('fornecedores/excluir/<int:pk>/', views.fornecedor_delete, name='fornecedor_delete'),
    path('custos/', views.custo_list, name='custo_list'),
    path('custos/novo/', views.custo_create, name='custo_create'),
    path('sync/', views.sync_financeiro, name='sync'),
    path('relatorio/mei/', views.relatorio_mei, name='relatorio_mei'),
]
