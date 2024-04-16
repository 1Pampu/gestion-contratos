from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Inmueble(models.Model):
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    partida = models.IntegerField(primary_key=True, unique=True, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    composicion = models.TextField(max_length=500)
    condicion = models.TextField(max_length=2000)

    def __str__(self):
        parte1= str(self.partida)[:3]
        parte2= str(self.partida)[3:9]
        parte3= str(self.partida)[9]
        partida_formateada = f"{parte1}-{parte2}-{parte3}"
        return partida_formateada