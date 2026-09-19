from django.db import models
from ubicaciones.models import Agencia
from django.contrib.auth.models import User
from uuid import uuid4

ESTADOS_PAQUETE = (
    ("registrado","Registrado"),
    ("cancelado", "Cancelado"),
    ("en_transito", "En Transito"),
    ("disponible", "Disponible"),
    ("entregado", "Entregado"),
    ("extraviado", "Extraviado"),
    ("en_agencia", "En Agencia")
)

class GuiaEnvio(models.Model):
    numero_guia = models.CharField(max_length=30, null=True, blank=True)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="remitentes")
    destinatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="destinatarios")

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="envios",)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    agencia_origen = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name="envio_agencia_origen" )
    agencia_destino = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name="envio_agencia_destino")

    peso_kg = models.DecimalField(decimal_places=2, max_digits=7)

    monto_bolivares = models.DecimalField(decimal_places=2, max_digits=7)
    monto_usd = models.DecimalField(decimal_places=2, max_digits=7)

    estado_actual = models.CharField(max_length=50, choices=ESTADOS_PAQUETE, default='registrado')

    def save(self, *args, **kwards):
        if not self.numero_guia:
            self.numero_guia =  uuid4().hex[:8].upper()

        super().save(*args,**kwards)

        if self.pk is None:
            HistorialSeguimiento.objects.create(
                guia=self,
                estado=self.estado_actual,
                actualiado_por=self.creado_por,
                observacion="El producto se ha registrado satisfactoriamente",
            )

    
class HistorialSeguimiento(models.Model):
    guia = models.ForeignKey(GuiaEnvio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADOS_PAQUETE, default='registrado')
    observacion = models.TextField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    actualiado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# Create your models here.
