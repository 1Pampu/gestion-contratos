from django.db import models
from datetime import timedelta
from personas.models import Persona

# Create your models here.
class Inmueble(models.Model):
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    num_partida = models.CharField(max_length=15)
    composicion = models.TextField(max_length=500)

    def __str__(self):
        return self.num_partida

class Contrato(models.Model):
    locador = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locador')
    locatario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locatario')
    garantia = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_garantia')
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    condicion = models.TextField(max_length=2000)
    fecha_inicio = models.DateField()
    duracion = models.IntegerField()
    fecha_finalizacion = models.DateField(null=True, blank=True)

    def calcular_fin(self):
        if self.fecha_inicio and self.duracion:
            duracion_dias = self.duracion * 30
            fecha_finalizacion = self.fecha_inicio + timedelta(days=duracion_dias)
            return fecha_finalizacion
        return None

    def save(self, *args, **kwargs):
        self.fecha_finalizacion = self.calcular_fin()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.locador} - {self.locatario} - {self.inmueble}'