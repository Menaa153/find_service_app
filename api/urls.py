from django.urls import path
#from .views import RegisterView, login_user
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    path('cambiar-rol/', views.cambiar_rol, name='cambiar_rol'),
    path('buscar-prestadores/', views.buscar_prestadores_cercanos, name='buscar_prestadores'),
    path('convertir-a-prestador/', views.convertir_a_prestador, name='convertir_a_prestador'),
    path('perfil/', views.obtener_perfil, name='perfil'),
]
