from django.db import models

# Create your models here.
class Inmueble(models.Model):
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    num_partida = models.CharField(max_length=15)
    composicion = models.TextField(max_length=500)
    condicion = models.TextField(max_length=2000)

    def __str__(self):
        return self.num_partida