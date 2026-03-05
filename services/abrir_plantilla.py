import os
from configs.manager_doc_config import get_ruta_a_la_plantilla_de_word
from docx import Document

from configs.manager_doc_config import get_ruta_a_la_plantilla_de_word


def abrir_plantilla() -> Document:
    """Abre el documento plantilla de DORIS y devuelve un objeto Document.

    Descripción:
        Esta función carga el documento plantilla de Word ubicado en la carpeta
        de plantillas para ser utilizado en la generación de documentos de
        despliegue de sondas DORIS.

    Retorna:
        Document: Un objeto Document de python-docx con la plantilla cargada."""
    
    # Construir la ruta al archivo plantilla
    ruta_plantilla = get_ruta_a_la_plantilla_de_word() 
    
    # Abrir y retornar el documento
    try:
        documento = Document(ruta_plantilla)    
    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        raise e
    
    return documento
