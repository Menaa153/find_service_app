from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reserva
from .serializers import ReservaSerializer

class ReservaCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Aquí asumimos que el cliente y prestador se pasan como datos en el body
        data = request.data
        # Verifica los datos que debes recibir del cliente
        cliente = request.user  # Suponiendo que el cliente está autenticado
        prestador = data.get("prestador_id")
        fecha = data.get("fecha")
        hora = data.get("hora")

        # Crear la reserva
        reserva = Reserva.objects.create(
            cliente=cliente,
            prestador_id=prestador,
            fecha=fecha,
            hora=hora,
        )

        # Serializar la reserva y devolver la respuesta
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ReservasClienteView(APIView):
    permission_classes = [IsAuthenticated]  # Solo los usuarios autenticados pueden acceder a este endpoint

    def get(self, request):
        cliente = request.user  # Obtenemos el usuario actual
        reservas = Reserva.objects.filter(cliente=cliente)  # Filtramos las reservas por cliente
        serializer = ReservaSerializer(reservas, many=True)  # Serializamos las reservas
        return Response(serializer.data)  # Devolvemos las reservas como JSON
