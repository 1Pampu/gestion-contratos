from django.db import models
from datetime import timedelta
from personas.models import Persona
from inmuebles.models import Inmueble

# Create your models here.
class Contrato(models.Model):
    locador = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locador', null=True, blank=True)
    locatario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locatario', null=True, blank=True)
    garantia = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_garantia', null=True, blank=True)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField()
    duracion = models.IntegerField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    docx = models.FileField(upload_to='documents/contratos/%Y/%m', null=True, blank=True)
    active = models.BooleanField(default=True)

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