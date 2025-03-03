from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from .views import RegisterView, login_user
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    path('cambiar-rol/', views.cambiar_rol, name='cambiar_rol'),
    path('buscar-prestadores/', views.buscar_prestadores_cercanos, name='buscar_prestadores'),
    path('convertir-a-prestador/', views.convertir_a_prestador, name='convertir_a_prestador'),
    path('perfil/', views.obtener_perfil, name='perfil'),
    path('upload-profile-picture/', views.UploadProfilePicture.as_view(), name='upload-profile-picture'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
