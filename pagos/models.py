from django.db import models
from contratos.models import Contrato
from dateutil.relativedelta import relativedelta
import os

# Create your models here.
class Pago(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='pagos')
    num_cuota = models.IntegerField()
    desde = models.DateField(null=True, blank=True)
    hasta = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vencido = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True)
    factura = models.FileField(upload_to='facturas/%Y/%m', null=True, blank=True)

    def __str__(self):
        return f'{self.contrato.id} - Cuota {self.num_cuota}'

    def calcular_desde_y_hasta(self):
        # ! QUE HACER SI EL DIA DE PAGO ES MAYOR AL DIA DE INICIO DEL CONTRATO
        mes = self.num_cuota - 1
        desde = self.contrato.fecha_inicio + relativedelta(months=+mes, day=self.contrato.dia_pago)
        hasta = desde + relativedelta(days=self.contrato.plazo_pago)
        return desde, hasta

    def save(self, *args, **kwargs):
        self.desde, self.hasta = self.calcular_desde_y_hasta()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.factura:
            if os.path.isfile(self.factura.path):
                os.remove(self.factura.path)

        super().delete(*args, **kwargs)