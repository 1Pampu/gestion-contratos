from django.db import models

# Create your models here.
class Contrato(models.Model):
    inicio = models.DateField()
    finalizacion = models.DateField()
    propiedad = models.CharField(max_length=200)
    propietario = models.CharField(max_length=200)
    inquilino = models.CharField(max_length=200)
    precio = models.IntegerField()

    def __str__(self):
        return self.propiedad