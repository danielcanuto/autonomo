from django.urls import path
from . import views

app_name = 'encomendas'

urlpatterns = [
    path('', views.encomenda_list, name='encomenda_list'),
    path('nova/', views.encomenda_create, name='encomenda_create'),
    path('<int:pk>/', views.encomenda_detail, name='encomenda_detail'),
    path('<int:pk>/editar/', views.encomenda_update, name='encomenda_update'),
    path('<int:pk>/fechar/', views.encomenda_fechar_pedido, name='encomenda_fechar_pedido'),
    path('<int:pk>/pagar/', views.registrar_pagamento_encomenda, name='registrar_pagamento_encomenda'),
    path('render-form-step/', views.render_form_step, name='render_form_step'),
]
