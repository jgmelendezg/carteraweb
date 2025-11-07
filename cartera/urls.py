from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_cartera),
    path('dashboard/', views.dashboard_cartera, name='dashboard_cartera'),
    path('detalle/', views.detalle_cliente, name='detalle_cliente'),
    path('pdf-detalle/', views.pdf_detalle_cliente, name='pdf_detalle_cliente'),
]