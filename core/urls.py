from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contratos.urls')),
    path('personas/', include('personas.urls')),
    path('inmuebles/', include('inmuebles.urls')),
    path('config/', include('configuraciones.urls')),
    path('pagos/', include('pagos.urls')),
]
