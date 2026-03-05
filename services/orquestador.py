######################################### NO TOCAR ##########################################
import os
import sys

# Agrega la ruta raíz del proyecto si no está
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from configs.manager_doc_config import *
from services.leer_excel import *
from services.crear_diccionario_del_df_excel_maestro import *   
from services.navegacion import obtener_coords_ordenadas_distancias_y_tiempos
from services.estimar_fecha_y_hora_de_embarque import estimar_fecha_y_hora_de_embarque

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from services.get_lon_lat_max_and_min import get_lon_lat_max_and_min
from services.gra_mapa_cartopy import graficar_mapa_cartopy
from services.gra_coordenadas import graficar_coordenadas
from services.cargar_datos_de_batimetria import cargar_datos_de_batimetria
from services.gra_batimetria_en_mapa import graficar_batimetria_en_mapa
from services.dar_formato_al_mapa import dar_formato_al_mapa
from services.guardar_figura import guardar_figura

from services.abrir_plantilla import *
from services.reemplazar_en_plantilla import reemplazar_en_word, rellenar_tabla
from services.guardar_documento import guardar_documento
##############################################################################################


def crear_plan_de_crucero():
        
    dic = crear_diccionario_del_df_excel_maestro()
    navegacion = obtener_coords_ordenadas_distancias_y_tiempos(campania= get_hacer_planes())
    estimar_fecha_y_hora_de_embarque(campania= get_hacer_planes())
    datos_de_batimetria = cargar_datos_de_batimetria()
    
    # Pendiente pasar toda esta parte de la figura a un manager
    fig, axe = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
    lon_min, lon_max, lat_min, lat_max = get_lon_lat_max_and_min(navegacion)
    graficar_mapa_cartopy(axe, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
    graficar_batimetria_en_mapa(axe, datos_de_batimetria, navegacion)
    graficar_coordenadas(axe, navegacion)
    # Aplicar el formato al mapa con las propiedades definidas
    propiedades_de_mapa = {"obj_axes": axe}
    dar_formato_al_mapa(propiedades_de_mapa)
    plt.close(fig) # Cerrar la figura para evitar que se muestre en pantalla
    ruta_a_figura = guardar_figura(fig, f"{get_hacer_planes()[0]}.png")
    dic["<<fig_mapa_derrotero>>"] = ruta_a_figura
    
    doc = abrir_plantilla()
    new_doc = reemplazar_en_word(doc, dic)
    new_doc = rellenar_tabla(new_doc, "<<tabla1>>", dic["<<tabla1>>"])
    new_doc = rellenar_tabla(new_doc, "<<tabla2>>", dic["<<tabla2>>"])
    guardar_documento(new_doc,nombre_archivo = f"{get_hacer_planes()[0]}.docx")
    
    