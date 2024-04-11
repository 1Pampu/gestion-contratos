from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.IntegerField(validators=[MinValueValidator(1000000), MaxValueValidator(99999999)], primary_key=True, unique=True)
    email = models.EmailField(max_length=75)
    celular = models.CharField(max_length=18)
    domicilio = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)

    def __str__(self):
        return self.dni