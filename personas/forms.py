from django import forms
from .models import Persona

# Widgets Classes
widget_text = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
widget_dni = forms.TextInput(attrs={'class': 'form-control', 'list': 'persons_list', 'autocomplete': 'off'})

# Create your forms here.
class PersonaForm(forms.ModelForm):

    nombre = forms.CharField(widget=widget_text)
    dni = forms.CharField(widget=widget_dni)
    email = forms.EmailField(widget=widget_text)
    celular = forms.CharField(widget=widget_text)
    domicilio = forms.CharField(widget=widget_text)
    ciudad = forms.CharField(widget=widget_text)

    class Meta:
        model = Persona
        fields = ['nombre', 'dni', 'email', 'celular', 'domicilio', 'ciudad']