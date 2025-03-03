from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservaCreateView.as_view(), name='create_reserva'),  # Definir endpoint para POST
    path('cliente/', views.ReservasClienteView.as_view(), name='reservas_cliente'),
]
