from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Reserva(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservas_cliente")
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservas_prestador")
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=255)
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva de {self.cliente.username} con {self.prestador.username} el {self.fecha} a las {self.hora}"
