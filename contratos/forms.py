from django import forms
from .models import Contrato

# Widgets Classes
widget_integer = forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
widget_date = forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'})

# Create your forms here.
class ContratoForm(forms.ModelForm):

    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {
            'fecha_inicio': widget_date,
            'duracion': widget_integer,
            'dia_pago': widget_integer,
            'plazo_pago': widget_integer,
        }
