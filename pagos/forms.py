from django import forms
from datetime import date

class PagarForm(forms.Form):
    fecha_pago = forms.DateField(widget=forms.DateInput(
        attrs={
            'type': 'date',
            'value': date.today()
            }))
    salario_basico = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(
        attrs={
            'step': '0.01',
            'min': '0',
            'max': '9999999999',
               }))