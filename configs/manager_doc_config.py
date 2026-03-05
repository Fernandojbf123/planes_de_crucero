import os
import dotenv
import importlib
import configs.configuracion_documentos
importlib.reload(configs.configuracion_documentos)

dotenv.load_dotenv()  # Carga las variables de entorno desde el archivo .env

def get_usar_NAS():
    """Obtiene un valor de la configuración general de forma dinámica"""
    return configs.configuracion_documentos.usar_NAS

def get_ruta_a_la_base_de_datos():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_la_base_de_datos
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_a_carpeta_de_las_figuras():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_las_figuras
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_a_carpeta_de_guardado_del_documento():
    """Obtiene un valor de la configuración general de forma dinámica"""
    ruta_al_NAS = os.getenv("ruta_al_NAS")
    carpeta = configs.configuracion_documentos.ruta_a_carpeta_de_guardado_del_documento
    if get_usar_NAS() and ruta_al_NAS:
        ruta_completa = os.path.join(ruta_al_NAS, carpeta)   
    else:
        ruta_completa = carpeta  # Si no se encuentra la variable de entorno, usar la ruta relativa     
    return ruta_completa

def get_ruta_a_la_plantilla_de_word():
    return configs.configuracion_documentos.ruta_a_la_plantilla_de_word

def get_ruta_a_datos_batimetria():
    return configs.configuracion_documentos.ruta_a_la_batimetria

def get_velocidad_de_embarcacion():
    return configs.configuracion_documentos.velocidad_de_embarcacion

def get_hacer_planes():
    return configs.configuracion_documentos.hacer_planes

def get_estilo_normal():
    return configs.configuracion_documentos.estilo_normal

def get_estilo_texto_tablas_centrado():
    return configs.configuracion_documentos.estilo_texto_tablas_centrado

def get_estilo_texto_tablas_justificado():
    return configs.configuracion_documentos.estilo_texto_tablas_justificado

def get_estilo_pie_de_imagen():
    return configs.configuracion_documentos.estilo_pie_de_imagen

