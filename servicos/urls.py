from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.servico_list, name='servico_list'),
    path('novo/', views.servico_create, name='servico_create'),
    path('categoria/nova/', views.categoria_create, name='categoria_create'),
]
