from django.urls import path
from . import views

app_name = 'orcamentos'

urlpatterns = [
    path('', views.orcamento_list, name='orcamento_list'),
    path('<int:pk>/', views.orcamento_detail, name='orcamento_detail'),
    path('novo/', views.orcamento_create, name='orcamento_create'),
    path('<int:pk>/editar/', views.orcamento_update, name='orcamento_update'),
    path('<int:pk>/converter/', views.converter_em_contrato, name='converter_em_contrato'),
    path('<int:pk>/pagamento/', views.orcamento_pagamento_create, name='orcamento_pagamento_create'),
]
