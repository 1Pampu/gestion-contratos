from io import BytesIO
from docx import Document
from django.http import HttpResponse
from num2words import num2words
import locale
from personas.utils import verificar_persona
from inmuebles.utils import verificar_inmueble

def autocompletar_docx(template_path, contrato):
    # Abrir el documento
    doc = Document(template_path)

    datos = {
        # Locador Info
        'nombre_locador' : contrato.locador.nombre.upper(),
        'dni_locador' : contrato.locador.dni,
        'email_locador' : contrato.locador.email,
        'celular_locador' : contrato.locador.celular,
        'domicilio_locador' : contrato.locador.domicilio,
        'ciudad_locador' : contrato.locador.ciudad,

        # Locatario Info
        'nombre_locatario' : contrato.locatario.nombre.upper(),
        'dni_locatario' : contrato.locatario.dni,
        'email_locatario' : contrato.locatario.email,
        'celular_locatario' : contrato.locatario.celular,
        'domicilio_locatario' : contrato.locatario.domicilio,
        'ciudad_locatario' : contrato.locatario.ciudad,

        # Garantia Info
        'nombre_garantia' : contrato.garantia.nombre.upper(),
        'dni_garantia' : contrato.garantia.dni,
        'email_garantia' : contrato.garantia.email,
        'celular_garantia' : contrato.garantia.celular,
        'domicilio_garantia' : contrato.garantia.domicilio,
        'ciudad_garantia' : contrato.garantia.ciudad,

        # Inmueble Info
        'direccion_inmueble' : contrato.inmueble.direccion,
        'ciudad_inmueble' : contrato.inmueble.ciudad,
        'num_partida' : contrato.inmueble,
        'composicion_inmueble' : contrato.inmueble.composicion,

        # Contrato Info
        'fecha_inicio' : fecha_a_texto(contrato.fecha_inicio),
        'fecha_fin' : fecha_a_texto(contrato.fecha_finalizacion),
        'duracion_str' : numero_a_texto(contrato.duracion),
    }

    # Iterar sobre los párrafos del documento
    for paragraph in doc.paragraphs:
        for key, value in datos.items():
            # Reemplazar el texto entre corchetes con los datos proporcionados
            if f"[{key}]" in paragraph.text:
                run_list = paragraph.runs
                for run in run_list:
                    if f"[{key}]" in run.text:
                        run.text = run.text.replace(f"[{key}]", str(value))

    # Guardar el documento en un buffer de BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    num_partida = datos['num_partida']
    # Crear una respuesta HTTP para el archivo descargable
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=CONTRATO DE LOCACIÓN {num_partida}.docx'

    return response

def numero_a_texto(numero):
    texto = num2words(numero, lang='es')
    return texto

def fecha_a_texto(date):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    string = date.strftime("%d de %B de ")
    anio = numero_a_texto(date.year)
    return string + anio

def validaciones_contrato(request, validacion):
    # VALIDACION    1            2           3
    url = "?"
    personas = ['locador', 'locatario', 'garantia']
    x = 0
    for i in personas:
        dni = request.GET.get(i)
        if not verificar_persona(dni):
            return False, i
        url += f'{i}={dni}&'
        if x == (validacion-1):
            break
        x += 1

    if validacion == 4:
        partida = request.GET.get('inmueble')
        if not verificar_inmueble(partida):
            return False, "inmueble"
        url += f'inmueble={partida}'

    return True, url