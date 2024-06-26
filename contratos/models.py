from django.db import models
from dateutil.relativedelta import relativedelta
from personas.models import Persona
from inmuebles.models import Inmueble
import os

# Create your models here.
class Contrato(models.Model):
    locador = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locador', null=True, blank=True)
    locatario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_locatario', null=True, blank=True)
    garantia = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_garantia', null=True, blank=True)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    duracion = models.IntegerField()
    docx = models.FileField(upload_to='contratos/%Y/%m', null=True, blank=True)
    dia_pago = models.IntegerField(default=15)
    plazo_pago = models.IntegerField(default=7)
    porcentaje_pago = models.DecimalField(max_digits=4, decimal_places=2)

    def calcular_fin(self):
        if self.fecha_inicio and self.duracion:
            fecha_finalizacion = self.fecha_inicio + relativedelta(months=self.duracion)
            return fecha_finalizacion
        return None

    def save(self, *args, **kwargs):
        self.fecha_finalizacion = self.calcular_fin()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.docx:
            if os.path.isfile(self.docx.path):
                os.remove(self.docx.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.locador} - {self.locatario} - {self.inmueble}'

class ContratoDetalle(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='contrato_detalle')
    composicion = models.TextField(max_length=500, default='', null=True, blank=True)
    condicion = models.TextField(max_length=2000, default='', null=True, blank=True)

    def __str__(self):
        return f'Detalle del contrato: {self.contrato.id}'