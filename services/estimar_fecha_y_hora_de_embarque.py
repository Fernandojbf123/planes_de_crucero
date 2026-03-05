
import numpy as np
import pandas as pd
from configs.manager_doc_config import get_velocidad_de_embarcacion
from services.leer_excel import leer_excel
from services.convertir_coordenadas import convertir_cualquier_coordenada_a_grados_decimales
from services.calcular_distancia_entre_dos_coordenadas import calcular_distancia_entre_dos_coordenadas


def estimar_fecha_y_hora_de_embarque(campania = None):
    df_campanias = leer_excel(nombre_de_hoja="campanias", header=0)
    df_campanias = df_campanias[df_campanias["campania"].isin(campania)]
    sitio_de_embarque = df_campanias["sitio_de_embarque"].iloc[0]
    sitio_de_desembarque = df_campanias["sitio_de_desembarque"].iloc[0]
    
    # Cargar las coordenadas de los puertos para posterioremnte elegir las del puerto de embarque y desembarque
    df_ptos = leer_excel(nombre_de_hoja="sitios_de_embarque", header=0) 
    df_embarque = df_ptos[df_ptos["nombre"].str.strip() == sitio_de_embarque.strip()].iloc[0] # busco el puerto de embarque
    lat_embarque = round(df_embarque["latitud"],6)
    lon_embarque = round(df_embarque["longitud"],6)
    
    # ordeno las maniobras realizadas por hora
    df_campanias["fecha_y_hora_de_maniobra"] = pd.to_datetime(df_campanias["fecha_y_hora_de_maniobra"], format="%d/%m/%Y %H:%M", utc=True)
    df_campanias.sort_values(by="fecha_y_hora_de_maniobra", inplace=True)
    
    # Ahora busco las coordenadas de cada maniobra
    lat_plan = round(df_campanias["lat_plan"].apply(lambda x: convertir_cualquier_coordenada_a_grados_decimales(x)), 6)
    lon_plan = round(df_campanias["lon_plan"].apply(lambda x: convertir_cualquier_coordenada_a_grados_decimales(x)), 6)
    localizaciones = df_campanias["localizacion"].tolist()
    
    velocidad_nudos = get_velocidad_de_embarcacion()
    
    latitudes = [lat_embarque] + [lat_plan.tolist()[0]]
    longitudes = [lon_embarque] + [lon_plan.tolist()[0]]
    
    x_origen = longitudes[0]
    y_origen = latitudes[0]
    x_dest = longitudes[1]
    y_dest = latitudes[1]
    resultado = calcular_distancia_entre_dos_coordenadas(lon_fin=x_dest, lat_fin=y_dest, lon_ini=x_origen, lat_ini=y_origen, velocidad_nudos=velocidad_nudos)
    # Aquí puedes almacenar o imprimir el resultado según tus necesidades
    
    fecha_y_hora_de_la_primera_maniobra = df_campanias["fecha_y_hora_de_maniobra"].iloc[0]
    horas_de_viaje = resultado["tiempo_h"] # tiempo de viaje desde el puerto de embarque hasta las coordenadas de la primera maniobra
    fecha_y_hora_de_embarque = fecha_y_hora_de_la_primera_maniobra - pd.Timedelta(hours=horas_de_viaje)
    fecha_y_hora_de_embarque = fecha_y_hora_de_embarque.replace(second=0, microsecond=0) # redondeo a la hora exacta
    print(f"Hora de embarque aprox (UTC): {fecha_y_hora_de_embarque:%d-%m-%Y %H:%M}")