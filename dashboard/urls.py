from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('painel/', views.index, name='painel'),
]
