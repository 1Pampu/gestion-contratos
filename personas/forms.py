from django import forms
from .models import Persona

# Widgets Classes
widget_text = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
widget_dni = forms.TextInput(attrs={'class': 'form-control', 'list': 'persons_list', 'autocomplete': 'off'})

# Create your forms here.
class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'nombre': widget_text,
            'dni': widget_dni,
            'email': widget_text,
            'celular': widget_text,
            'domicilio': widget_text,
            'ciudad': widget_text
        }