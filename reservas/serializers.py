from rest_framework import serializers
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'cliente', 'prestador', 'fecha', 'hora', 'ubicacion', 'confirmada']
