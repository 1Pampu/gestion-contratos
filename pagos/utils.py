from django.conf import settings
from docxtpl import DocxTemplate
import subprocess
import os


def generar_factura(pago):
    contrato = pago.contrato
    inmueble = contrato.inmueble

    doc = DocxTemplate('plantillas_docx/facturas.docx')

    datos = {
        'locatario_nombre': contrato.locatario.nombre,
        'locatario_direccion': contrato.locatario.domicilio,
        'locatario_email': contrato.locatario.email,
        'locatario_celular': contrato.locatario.celular,

        'fecha_pago': pago.fecha_pago,
        'vencimiento': pago.hasta,

        'direccion_inmueble': inmueble.direccion,

        'salario': pago.salario_basico,
        'pago': contrato.porcentaje_pago,
        'monto': pago.monto,
    }
    doc.render(datos)

    temp_folder = os.path.join(settings.BASE_DIR, 'temp')
    os.makedirs(temp_folder)
    file = f'Factura Contrato{contrato.id}-Couta{pago.num_cuota}'
    docx_file_path = os.path.join(temp_folder, f'{file}.docx')
    doc.save(docx_file_path)
    subprocess.check_output(['libreoffice', '--convert-to', 'pdf', '--outdir', temp_folder, f'{docx_file_path}'])
    pago.factura.save(f'{file}.pdf', open(f'{temp_folder}/{file}.pdf', 'rb'))

    os.remove(docx_file_path)
    os.remove(f'{temp_folder}/{file}.pdf')
    os.rmdir(temp_folder)

    return True