from django.urls import path
from .views import index, nuevo_contrato, contrato

urlpatterns = [
    path('', index, name='index'),
    path('nuevo_contrato/', nuevo_contrato, name='nuevo_contrato'),
    path('contrato/<int:id_contrato>/', contrato, name='contrato')
]