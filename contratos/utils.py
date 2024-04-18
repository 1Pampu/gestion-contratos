from io import BytesIO
from docx import Document
from django.http import HttpResponse
from num2words import num2words
import locale
from personas.utils import verificar_persona
from inmuebles.utils import verificar_inmueble

def autocompletar_docx(template_path, datos):
    # Abrir el documento
    doc = Document(template_path)

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
    for i in range(1, validacion + 1):
        dni = request.GET.get(personas[i-1])
        if not verificar_persona(dni):
            return False, personas[i-1]
        url += f'{personas[i-1]}={dni}&'
        if i == validacion:
            break

    if validacion == 4:
        partida = request.GET.get('inmueble')
        if not verificar_inmueble(partida):
            return False, "inmueble"
        url += f'inmueble={partida}'

    return True, url