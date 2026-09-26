from django.db import models

# Create your models here.
class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return f"{self.nombre}"

class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    class Meta:
            verbose_name = "Ciudad"
            verbose_name_plural = "Ciudades"

    def __str__(self):
            return f"{self.nombre} - {self.estado.nombre}"

class Agencia(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.RESTRICT)
    rif = models.CharField(max_length=50)
    def __str__(self):
            return f"{self.nombre} - {self.rif} - {self.ciudad.nombre}"

    class Meta:
            verbose_name = "Agencia"
            verbose_name_plural = "Agencias"

