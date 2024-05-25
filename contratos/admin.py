from django.contrib import admin
from .models import Contrato, ContratoDetalle

# Register your models here.
admin.site.register(Contrato)
admin.site.register(ContratoDetalle)