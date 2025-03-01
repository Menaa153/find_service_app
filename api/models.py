
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models

# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()



class CustomUser(AbstractUser):
    CLIENTE = 'cliente'
    PRESTADOR = 'prestador'

    ROLE_CHOICES = [
        (CLIENTE, 'Cliente'),
        (PRESTADOR, 'Prestador de Servicio'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENTE)

    # nuevos campos
    first_name = models.CharField(max_length=50, blank=True, null=True)  # Nombre
    last_name = models.CharField(max_length=50, blank=True, null=True)  # Apellido
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True) 

    # datos adicionales para prestadores
    categoria = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    location = models.PointField(geography=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} - {self.role}"
