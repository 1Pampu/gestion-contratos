from django.conf import settings
from docxtpl import DocxTemplate
from configuraciones.utils import delete_folder_and_content
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

    # Libreoffice Installation Path
    libreoffice = settings.LIBREOFFICE

    # Create Temp folder
    temp_folder = os.path.join(settings.BASE_DIR, 'temp')
    os.makedirs(temp_folder)

    try:
        # Create Completed Docx File
        file = f'Factura-Contrato{contrato.id}-Couta{pago.num_cuota}'
        docx_file_path = os.path.join(temp_folder, f'{file}.docx')
        doc.save(docx_file_path)

        # Convert to Pdf
        subprocess.check_output([libreoffice, '--headless', '--convert-to', 'pdf', '--outdir', temp_folder, docx_file_path])
        pdf_path = os.path.join(temp_folder, f'{file}.pdf')
        pago.factura.save(f'{file}.pdf', open(pdf_path, 'rb'))

    finally:
        delete_folder_and_content(temp_folder)

    return True