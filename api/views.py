from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Producto, CustomUser
from .serializer import ProductoSerializer

from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance






User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

"""
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


@api_view(['POST'])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)
    if user is None:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.role,  # Enviar rol en la respuesta
        "nombre": user.first_name
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_rol(request):
    user = request.user
    nuevo_rol = request.data.get("role")

    if nuevo_rol not in [User.CLIENTE, User.PRESTADOR]:
        return Response({"error": "Rol inválido"}, status=status.HTTP_400_BAD_REQUEST)

    user.role = nuevo_rol
    user.save()
    return Response({"message": f"Rol cambiado a {nuevo_rol}"}, status=status.HTTP_200_OK)
    




@api_view(['GET'])
def buscar_prestadores_cercanos(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    categoria = request.query_params.get('categoria', "").strip().lower()  # Convertimos a minusculas

    if not lat or not lon or not categoria:
        return Response({"error": "Se requieren latitud, longitud y categoría"}, status=400)

    user_location = Point(float(lon), float(lat), srid=4326)

    # Filtrar prestadores con la categoría buscada
    prestadores = User.objects.filter(
        role=User.PRESTADOR,
        location__isnull=False,  # Solo prestadores con ubicacion
        categoria__iexact=categoria  # Coincidencia exacta sin importar mayusculas/minusculas
    ).annotate(
        distancia=Distance('location', user_location)
    ).order_by('distancia')[:5]  # Solo los 5 más cercanos

    resultado = [
        {
            "id": p.id,
            "username": p.first_name,
            "email": p.email,
            "categoria": p.categoria,
            "distancia_km": p.distancia.km,
            "descripcion": p.descripcion
        } 
        for p in prestadores
    ]

    return Response(resultado, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def convertir_a_prestador(request):
    user = request.user

    # Obtener datos del formulario
    categoria = request.data.get("categoria")
    descripcion = request.data.get("descripcion")
    lat = request.data.get("lat")
    lon = request.data.get("lon")

    # Validar que los datos sean correctos
    if not categoria or not descripcion or not lat or not lon:
        return Response({"error": "Todos los campos son obligatorios"}, status=400)

    # Convertir el cliente en prestador
    user.role = User.PRESTADOR
    user.categoria = categoria
    user.descripcion = descripcion
    user.location = Point(float(lon), float(lat), srid=4326)
    user.save()

    return Response({"message": "Ahora eres un Prestador de Servicio"}, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # solo usuarios autenticados pueden acceder a su perfil
def obtener_perfil(request):
    user = request.user
    return Response({
        "username": user.first_name,
        "apellido": user.last_name,
        "email": user.email,
        "telefono": user.phone,
        "role": user.role,
        "descripcion" : user.descripcion,
        "ubicacion" : user.ubicacion,
    })
