from django import forms
from .models import Persona, Inmueble

# Widgets Classes
widget_select = forms.Select(attrs={'required': 'required', 'class': 'form-select'})
widget_text = forms.TextInput(attrs={'class': 'form-control'})
widget_textarea = forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
widget_integer = forms.NumberInput(attrs={'class': 'form-control'})
widget_date = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})

# Create your forms here.
class ContratoForm(forms.Form):

    locador = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False, widget=widget_select)
    nombre_locador = forms.CharField(max_length=100, required=False, widget=widget_text)
    dni_locador = forms.CharField(max_length=8, required=False, widget=widget_text)
    email_locador = forms.EmailField(max_length=75, required=False, widget=widget_text)
    celular_locador = forms.CharField(max_length=18, required=False, widget=widget_text)
    domicilio_locador = forms.CharField(max_length=200, required=False, widget=widget_text)
    ciudad_locador = forms.CharField(max_length=50, required=False, widget=widget_text)

    locatario = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False, widget=widget_select)
    nombre_locatario = forms.CharField(max_length=100, required=False, widget=widget_text)
    dni_locatario = forms.CharField(max_length=8, required=False, widget=widget_text)
    email_locatario = forms.EmailField(max_length=75, required=False, widget=widget_text)
    celular_locatario = forms.CharField(max_length=18, required=False, widget=widget_text)
    domicilio_locatario = forms.CharField(max_length=200, required=False, widget=widget_text)
    ciudad_locatario = forms.CharField(max_length=50, required=False, widget=widget_text)

    inmueble = forms.ModelChoiceField(queryset=Inmueble.objects.all(), required=False, widget=widget_select)
    direccion_inmueble = forms.CharField(max_length=200, required=False, widget=widget_text)
    ciudad_inmueble = forms.CharField(max_length=50, required=False, widget=widget_text)
    num_partida_inmueble = forms.CharField(max_length=15, required=False, widget=widget_text)
    composicion_inmueble = forms.CharField(max_length=500, widget=widget_textarea, required=False)

    garantia = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False, widget=widget_select)
    nombre_garantia = forms.CharField(max_length=100, required=False, widget=widget_text)
    dni_garantia = forms.CharField(max_length=8, required=False, widget=widget_text)
    email_garantia = forms.EmailField(max_length=75, required=False, widget=widget_text)
    celular_garantia = forms.CharField(max_length=18, required=False, widget=widget_text)
    domicilio_garantia = forms.CharField(max_length=200, required=False, widget=widget_text)
    ciudad_garantia = forms.CharField(max_length=50, required=False, widget=widget_text)

    condicion = forms.CharField(max_length=2000, widget=widget_textarea)
    fecha_inicio = forms.DateField(widget=widget_date)
    duracion = forms.IntegerField(widget=widget_integer)

    def clean(self):
        cleaned_data = super().clean()
        locador = cleaned_data.get('locador')
        nombre_locador = cleaned_data.get('nombre_locador')
        dni_locador = cleaned_data.get('dni_locador')
        email_locador = cleaned_data.get('email_locador')
        celular_locador = cleaned_data.get('celular_locador')
        domicilio_locador = cleaned_data.get('domicilio_locador')
        ciudad_locador = cleaned_data.get('ciudad_locador')

        locatario = cleaned_data.get('locatario')
        nombre_locatario = cleaned_data.get('nombre_locatario')
        dni_locatario = cleaned_data.get('dni_locatario')
        email_locatario = cleaned_data.get('email_locatario')
        celular_locatario = cleaned_data.get('celular_locatario')
        domicilio_locatario = cleaned_data.get('domicilio_locatario')
        ciudad_locatario = cleaned_data.get('ciudad_locatario')

        garantia = cleaned_data.get('garantia')
        nombre_garantia = cleaned_data.get('nombre_garantia')
        dni_garantia = cleaned_data.get('dni_garantia')
        email_garantia = cleaned_data.get('email_garantia')
        celular_garantia = cleaned_data.get('celular_garantia')
        domicilio_garantia = cleaned_data.get('domicilio_garantia')
        ciudad_garantia = cleaned_data.get('ciudad_garantia')

        inmueble = cleaned_data.get('inmueble')
        direccion_inmueble = cleaned_data.get('direccion_inmueble')
        ciudad_inmueble = cleaned_data.get('ciudad_inmueble')
        num_partida_inmueble = cleaned_data.get('num_partida_inmueble')
        composicion_inmueble = cleaned_data.get('composicion_inmueble')

        if not locador:
            if not nombre_locador:
                raise forms.ValidationError('Debe ingresar el nombre del locador')
            if not dni_locador:
                raise forms.ValidationError('Debe ingresar el DNI del locador')
            if not email_locador:
                raise forms.ValidationError('Debe ingresar el email del locador')
            if not celular_locador:
                raise forms.ValidationError('Debe ingresar el celular del locador')
            if not domicilio_locador:
                raise forms.ValidationError('Debe ingresar el domicilio del locador')
            if not ciudad_locador:
                raise forms.ValidationError('Debe ingresar la ciudad del locador')

        if not locatario:
            if not nombre_locatario:
                raise forms.ValidationError('Debe ingresar el nombre del locatario')
            if not dni_locatario:
                raise forms.ValidationError('Debe ingresar el DNI del locatario')
            if not email_locatario:
                raise forms.ValidationError('Debe ingresar el email del locatario')
            if not celular_locatario:
                raise forms.ValidationError('Debe ingresar el celular del locatario')
            if not domicilio_locatario:
                raise forms.ValidationError('Debe ingresar el domicilio del locatario')
            if not ciudad_locatario:
                raise forms.ValidationError('Debe ingresar la ciudad del locatario')

        if not garantia:
            if not nombre_garantia:
                raise forms.ValidationError('Debe ingresar el nombre de la garantía')
            if not dni_garantia:
                raise forms.ValidationError('Debe ingresar el DNI de la garantía')
            if not email_garantia:
                raise forms.ValidationError('Debe ingresar el email de la garantía')
            if not celular_garantia:
                raise forms.ValidationError('Debe ingresar el celular de la garantía')
            if not domicilio_garantia:
                raise forms.ValidationError('Debe ingresar el domicilio de la garantía')
            if not ciudad_garantia:
                raise forms.ValidationError('Debe ingresar la ciudad de la garantía')

        if not inmueble:
            if not direccion_inmueble:
                raise forms.ValidationError('Debe ingresar la dirección del inmueble')
            if not ciudad_inmueble:
                raise forms.ValidationError('Debe ingresar la ciudad del inmueble')
            if not num_partida_inmueble:
                raise forms.ValidationError('Debe ingresar el número de partida del inmueble')
            if not composicion_inmueble:
                raise forms.ValidationError('Debe ingresar la composición del inmueble')
