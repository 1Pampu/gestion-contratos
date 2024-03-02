from django import forms
from .models import Persona, Inmueble

# Create your forms here.
class ContratoForm(forms.Form):
    locador = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False,
        widget=forms.Select(attrs={'required': 'required'})
    )
    nombre_locador = forms.CharField(max_length=100, required=False)
    dni_locador = forms.CharField(max_length=8, required=False)
    email_locador = forms.EmailField(max_length=75, required=False)
    celular_locador = forms.CharField(max_length=18, required=False)
    domicilio_locador = forms.CharField(max_length=200, required=False)
    ciudad_locador = forms.CharField(max_length=50, required=False)

    locatario = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False,
        widget=forms.Select(attrs={'required': 'required'})
    )
    nombre_locatario = forms.CharField(max_length=100, required=False)
    dni_locatario = forms.CharField(max_length=8, required=False)
    email_locatario = forms.EmailField(max_length=75, required=False)
    celular_locatario = forms.CharField(max_length=18, required=False)
    domicilio_locatario = forms.CharField(max_length=200, required=False)
    ciudad_locatario = forms.CharField(max_length=50, required=False)

    inmueble = forms.ModelChoiceField(queryset=Inmueble.objects.all(), required=False,
        widget=forms.Select(attrs={'required': 'required'})
    )
    direccion_inmueble = forms.CharField(max_length=200, required=False)
    ciudad_inmueble = forms.CharField(max_length=50, required=False)
    num_partida_inmueble = forms.CharField(max_length=15, required=False)
    composicion_inmueble = forms.CharField(max_length=500, widget=forms.Textarea(), required=False)

    condicion = forms.CharField(max_length=2000, widget=forms.Textarea())
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    duracion = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        locador = cleaned_data.get('locador')
        dni_locador = cleaned_data.get('dni_locador')
        email_locador = cleaned_data.get('email_locador')
        celular_locador = cleaned_data.get('celular_locador')
        domicilio_locador = cleaned_data.get('domicilio_locador')
        ciudad_locador = cleaned_data.get('ciudad_locador')

        locatario = cleaned_data.get('locatario')
        dni_locatario = cleaned_data.get('dni_locatario')
        email_locatario = cleaned_data.get('email_locatario')
        celular_locatario = cleaned_data.get('celular_locatario')
        domicilio_locatario = cleaned_data.get('domicilio_locatario')
        ciudad_locatario = cleaned_data.get('ciudad_locatario')

        inmueble = cleaned_data.get('inmueble')
        direccion_inmueble = cleaned_data.get('direccion_inmueble')
        ciudad_inmueble = cleaned_data.get('ciudad_inmueble')
        num_partida_inmueble = cleaned_data.get('num_partida_inmueble')
        composicion_inmueble = cleaned_data.get('composicion_inmueble')

        if not locador:
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

        if not inmueble:
            if not direccion_inmueble:
                raise forms.ValidationError('Debe ingresar la dirección del inmueble')
            if not ciudad_inmueble:
                raise forms.ValidationError('Debe ingresar la ciudad del inmueble')
            if not num_partida_inmueble:
                raise forms.ValidationError('Debe ingresar el número de partida del inmueble')
            if not composicion_inmueble:
                raise forms.ValidationError('Debe ingresar la composición del inmueble')
