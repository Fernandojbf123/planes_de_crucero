import numpy as np
import pandas as pd
from configs.manager_doc_config import get_velocidad_de_embarcacion
from services.leer_excel import leer_excel
from services.convertir_coordenadas import convertir_cualquier_coordenada_a_grados_decimales
from services.calcular_distancia_entre_dos_coordenadas import calcular_distancia_entre_dos_coordenadas



def obtener_coords_ordenadas_distancias_y_tiempos(campania = None) -> dict:
    """Calcula la distancia navegada entre puntos consecutivos en un dataframe.
    
    Args:
        dataframe: Un dataframe con columnas 'lat_plan' y 'lon_plan' que contienen las coordenadas de los puntos.
    
    Returns:
        Un diccionario con las siguientes claves:
            - 'latitudes_recorridas': Lista de latitudes recorridas.
            - 'longitudes_recorridas': Lista de longitudes recorridas.
            - 'distancia_en_mn': Lista de distancias en millas náuticas entre puntos consecutivos.
            - 'tiempo_en_horas': Lista de tiempos en horas para recorrer cada segmento.
    
    Descripción:
        La función itera sobre las filas del dataframe, calcula la distancia entre cada punto y el siguiente utilizando la fórmula de Haversine, y almacena el resultado en una nueva columna. La última fila tendrá un valor de 0 o NaN para la distancia, ya que no hay un punto siguiente.
    """
    
    df_campanias = leer_excel(nombre_de_hoja="campanias", header=0)
    df_campanias = df_campanias[df_campanias["campania"].isin(campania)]
    
    # ordeno las maniobras realizadas por hora
    df_campanias["fecha_y_hora_de_plan"] = pd.to_datetime(df_campanias["fecha_y_hora_de_plan"], format="%d/%m/%Y %H:%M", utc=True)
    df_campanias.sort_values(by="fecha_y_hora_de_plan", inplace=True)
    df_campanias.reset_index(drop=True, inplace=True)
    
    sitio_de_embarque = df_campanias["sitio_de_embarque"].iloc[0]
    sitio_de_desembarque = df_campanias["sitio_de_desembarque"].iloc[0]
    
    # Cargar las coordenadas de los puertos para posterioremnte elegir las del puerto de embarque y desembarque
    df_ptos = leer_excel(nombre_de_hoja="sitios_de_embarque", header=0) 
    df_embarque = df_ptos[df_ptos["nombre"].str.strip() == sitio_de_embarque.strip()].iloc[0] # busco el puerto de embarque
    lat_embarque = round(df_embarque["latitud"],6)
    lon_embarque = round(df_embarque["longitud"],6)
    df_desembarque = df_ptos[df_ptos["nombre"].str.strip() == sitio_de_desembarque.strip()].iloc[0] # busco el puerto de desembarque
    lat_desembarque = round(df_desembarque["latitud"],6)
    lon_desembarque = round(df_desembarque["longitud"],6)
    
    
    
    # Ahora busco las coordenadas de cada maniobra
    lat_plan = round(df_campanias["lat_plan"].apply(lambda x: convertir_cualquier_coordenada_a_grados_decimales(x)), 6)
    lon_plan = round(df_campanias["lon_plan"].apply(lambda x: convertir_cualquier_coordenada_a_grados_decimales(x)), 6)
    localizaciones = df_campanias["localizacion"].tolist()
    seriales = df_campanias["serial_boya"].tolist()
    
    velocidad_nudos = get_velocidad_de_embarcacion()
    
    latitudes = [lat_embarque] + lat_plan.tolist() + [lat_desembarque]
    longitudes = [lon_embarque] + lon_plan.tolist() + [lon_desembarque]
    localizaciones = [df_embarque["nombre"]] + localizaciones + [df_desembarque["nombre"]]
    
    distancia_en_mn = []
    tiempo_en_horas = []
    for icoord in range(0,len(latitudes)-1):
        x_origen = longitudes[icoord]
        y_origen = latitudes[icoord]
        x_dest = longitudes[icoord+1]
        y_dest = latitudes[icoord+1]
        resultado = calcular_distancia_entre_dos_coordenadas(lon_fin=x_dest, lat_fin=y_dest, lon_ini=x_origen, lat_ini=y_origen, velocidad_nudos=velocidad_nudos)
        # Aquí puedes almacenar o imprimir el resultado según tus necesidades
        distancia_en_mn.append(resultado["distancia_mn"])
        tiempo_en_horas.append(resultado["tiempo_h"])
        
        
        
    output_dir = {
        "latitudes_plan": latitudes,
        "longitudes_plan": longitudes,
        "localizaciones": localizaciones,
        "seriales": seriales,
        "distancia_en_mn": np.round(distancia_en_mn, 2),
        "distancia_total_en_mn": round(sum(distancia_en_mn), 2),
        "tiempo_en_horas": np.round(tiempo_en_horas, 2),
        "tiempo_total_en_horas": round(sum(tiempo_en_horas), 2)
    }   
    
    return output_dir
    
    
    

    
