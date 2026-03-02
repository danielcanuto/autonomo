from django.urls import path
from . import views

app_name = 'contratos'

urlpatterns = [
    path('', views.contrato_list, name='contrato_list'),
    path('novo/', views.contrato_create, name='contrato_create'),
    path('editar/<int:pk>/', views.contrato_update, name='contrato_update'),
    path('pagamento/<int:pk>/', views.registrar_pagamento, name='registrar_pagamento'),
    path('<int:pk>/finalizar/', views.finalizar_contrato, name='finalizar_contrato'),
]
