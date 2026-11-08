from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CLIENTE = "cliente"
GERENTE = "gerente"
OPERADOR = "operador"
TRANSPORTISTA = "transportista"

roles = [
    (GERENTE, "Gerente"),
     (OPERADOR,"Operador Integral"),
     (TRANSPORTISTA, "Transportista"),
     (CLIENTE, "Cliente")
]

class Perfil(models.Model):
    cedula = models.CharField(max_length=9, unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(null=True, max_length=200, blank=True)
    rol = models.CharField(max_length=200, null=False, choices=roles, default=CLIENTE)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} {self.cedula} - {self.rol}"