from io import BytesIO
from docx import Document
from django.http import HttpResponse
from num2words import num2words

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