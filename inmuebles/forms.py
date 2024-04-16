from django import forms
from .models import Inmueble

# Widgets Classes
widget_text = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
widget_textarea = forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'autocomplete': 'off'})
widget_partida = forms.TextInput(attrs={'class': 'form-control', 'list': 'partidas_list',
                                        'autocomplete': 'off', 'pattern': "[0-9]{3}-[0-9]{6}-[0-9]{1}",
                                        'title': 'El número de partida debe tener el formato: xxx-xxxxxx-x',
                                        'maxlength': '12'})

# Create your forms here.
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = '__all__'
        widgets = {
            'direccion': widget_text,
            'ciudad': widget_text,
            'partida': widget_partida,
            'composicion': widget_textarea,
            'condicion': widget_textarea
        }