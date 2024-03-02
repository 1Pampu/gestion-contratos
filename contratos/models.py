from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    email = models.EmailField(max_length=75)
    celular = models.CharField(max_length=18)
    domicilio = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)

    def __str__(self):
        return self.dni

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
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    condicion = models.TextField(max_length=2000)
    fecha_inicio = models.DateField()
    duracion = models.IntegerField()
    fecha_finalizacion = models.DateField(null=True, blank=True)

    def calcular_fin(self):
        if self.fecha_inicio and self.duracion:
            fecha_finalizacion = self.fecha_inicio + self.duracion
            return fecha_finalizacion
        return None

    def save(self, *args, **kwargs):
        self.fecha_finalizacion = self.calcular_fin()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.locador} - {self.locatario} - {self.inmueble}'