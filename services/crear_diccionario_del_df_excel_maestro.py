import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import *
from services.convertir_coordenadas import convertir_cualquier_coordenada_a_grados_decimales
from services.navegacion import obtener_coords_ordenadas_distancias_y_tiempos

def realizado_o_realizada(maniobra: str) -> str:
    maniobra = maniobra.split(" ")[0]
    if "mantenimiento" in maniobra.lower() or "retiro" in maniobra.lower():
            return f"realizado"
    else:
        return f"realizada"

def crear_maniobra_str(maniobra: str) -> str:
    maniobra = maniobra.split(" ")[0]
    if "mantenimiento" in maniobra.lower() or "retiro" in maniobra.lower():
            return f"el {maniobra}"
    else:
        return f"la {maniobra}"

def aux_crear_datos_para_tabla1(df_campanias: pd.DataFrame) -> pd.DataFrame:

    
    df = df_campanias.reset_index(drop=True)
    df["localizacion"] = df["localizacion"].astype(str)
    secuencias = list(range(1, len(df)+1))
    localizaciones = df["localizacion"].tolist()
    lat_plan = [convertir_cualquier_coordenada_a_grados_decimales(coord) for coord in df["lat_plan"].tolist()]
    lon_plan = [convertir_cualquier_coordenada_a_grados_decimales(coord) for coord in df["lon_plan"].tolist()]

    tirante_disenio = [localizacion.split("-")[-1].replace("T","") if "doris" not in localizacion.lower() else None for localizacion in localizaciones]

    output_dic = {
        "<<secuencia>>": secuencias,
        "<<localizacion>>": localizaciones,
        "<<tirante_dis>>": tirante_disenio,
        "<<lat_plan>>": lat_plan,
        "<<lon_plan>>": lon_plan
    }
    return output_dic


def aux_crear_datos_para_tabla2(df_campanias: pd.DataFrame) -> pd.DataFrame:

    df = df_campanias.reset_index(drop=True)
    
    maniobras = df["maniobra"].tolist()
    
    pto_salida = df["sitio_de_embarque"].iloc[0]
    pto_llegada = df["sitio_de_desembarque"].iloc[0]
    
    secuencia = [1]
    actividad = [f"Salida desde {pto_salida}."]
    
    for it in range(len(maniobras)):
        maniobra = maniobras[it]
        maniobra = crear_maniobra_str(maniobra)
            
        localizacion = df["localizacion"].iloc[it]
        
        secuencia.append(secuencia[-1]+1)
        actividad.append(f"Travesía para {maniobra} de la {localizacion}.")
        
    secuencia.append(secuencia[-1]+1)
    actividad.append(f"Travesía hacia {pto_llegada}.")
    secuencia.append(secuencia[-1]+1)
    actividad.append(f"Llegada a {pto_llegada}.")
    
    output_dic = {
        "<<secuencia>>": secuencia,
        "<<actividad>>": actividad
    }
    
    return output_dic


def aux_parrafo3(df_campanias: pd.DataFrame) -> str:
    
    """"
    Así mismo, se realizará <<maniobra>> de la <<tipo_boya>> instalada en la localización <<localizacion_1>>
    texto = "<<maniobra>> de la <<tipo_boya>> instalada en la localización <<localizacion_1>>"
    
    """
    maniobras = df_campanias["maniobra"].tolist()
    localizaciones = df_campanias["localizacion"].tolist()
    
    texto = ""
    cantidad_maniobras = len(maniobras) 
    for it, (maniobra, localizacion) in enumerate(zip(maniobras,localizaciones)):
        maniobra_str = crear_maniobra_str(maniobra)
        
            
        if "doris" in localizacion:
            pass # Pendiente texto de las DORIS
        else:
            txt = f"{maniobra_str} {realizado_o_realizada(maniobra)} en la {localizacion}"
            
            if cantidad_maniobras == 1:
                texto += f"{txt}"
        
            elif cantidad_maniobras > 1:
                if it == cantidad_maniobras-1:
                    texto += f"y {txt}."
                else:
                    texto += f"{txt}, "
                
    return texto

def aux_parrafo2(df_campanias: pd.DataFrame, fecha_salida_str: str, hora_salida_cst: str) -> str:
    
    """
    Ejemplo de párrafo completo:
     
    La salida de la embarcación será de Tecolutla, Veracruz, el día 01 de noviembre de 2025 a las 6:30:00 a.m. CST, 
    para navegar rumbo a la localización BOT1-09-T50 y realizar la instalación de la boya con identificador (ID) TAB04742. 
    Posteriormente se navegará hacia el lugar de zarpe.
    
    Ejemplo de párrafo con las variables:
    La salida de la embarcación será de <<sitio_embarque>>, el día <<fecha_embarque>> a las <<hora_embarque>> CST, 
    para navegar rumbo a la localización <<localizacion>> para realizar <<maniobra>>, con identificador (ID) <<serial>>.
    Posteriormente se navegará hacia el lugar de zarpe.

    """
    sitio_de_embarque = df_campanias["sitio_de_embarque"].iloc[0]
    fecha_de_embarque = fecha_salida_str
    hora_de_embarque = hora_salida_cst
    
    localizaciones = df_campanias["localizacion"].tolist()
    maniobras = df_campanias["maniobra"].tolist()
    seriales = df_campanias["serial_boya"].tolist()
    

    texto = f"La salida de la embarcación será de {sitio_de_embarque}, el día {fecha_de_embarque} a las {hora_de_embarque} CST, para navegar rumbo a "
    
    cantidad_de_maniobras = len(maniobras) 
    if cantidad_de_maniobras == 1:
        maniobra_anterior_str = crear_maniobra_str(maniobras[0])
        if "doris" in localizaciones[0].lower():
            pass # Pendiente texto de las DORIS
        else: # texto para las boyas
            texto += f"la localización {localizaciones[0]} para realizar {maniobra_anterior_str} de la boya con identificador (ID) {seriales[0]} "
    
    elif cantidad_de_maniobras > 1:
        #Revisar que no se repitan las localizaciones, si se repiten, no repetir la localizacion en el texto, solo mencionar la maniobra y el serial de la boya.   
        # Condicion inincial para el primer elemento de la lista de maniobras y localizaciones.
        maniobra_anterior = maniobras[0].split(" ")[0]
        maniobra_anterior_str = crear_maniobra_str(maniobra_anterior)
            
        loc_anterior = localizaciones[0]
        if "doris" in loc_anterior.lower():
            pass # Pendiente texto de las DORIS
        else: # texto para las boyas
            texto += f"la localización {loc_anterior} para realizar {maniobra_anterior_str} con identificador (ID) {seriales[0]}, "
        
        # Iterar sobre el resto de las maniobras y localizaciones, empezando desde el segundo elemento (índice 1) de las listas.
        for iloc in range(1, len(localizaciones)):
        
            localizacion = localizaciones[iloc]
            maniobra = maniobras[iloc].split(" ")[0]
            maniobra_str = crear_maniobra_str(maniobra)
            serial = seriales[iloc]
            
            if "doris" in localizacion.lower():
                pass # Pendiente texto de las DORIS
            
            else: # texto para las boyas
                if localizacion == loc_anterior:
                    texto += f"así como para realizar {maniobra_str} con identificador (ID) {serial}, "
                    
                else:
                    loc_anterior = localizacion
                    texto += f"luego navegar rumbo a la localización {localizacion} para realizar {maniobra_str} con identificador (ID) {serial}"
        
    texto += ". Posteriormente se navegará hacia el lugar de zarpe."
                
    return texto

def aux_parrafo1(df_campanias: pd.DataFrame) -> str:
    
    """"
    Realizar la instalación de la Boya (Ocenografica/Metoceánica) Tipo X con identificador X correspondiente a la localización X
    
    texto = "<<maniobra>> de la Boya <<tipo_boya>> instalada en la localización <<localizacion>>"
    
    """
    
    tipos_de_boyas = {
        "BOT1": "Boya Oceanográfica Tipo 1",
        "BOT2": "Boya Oceanográfica Tipo 2",
        "BMT2": "Boya Metoceánica Tipo 2",
        "BMT3": "Boya Metoceánica Tipo 3"
    }
    
    maniobras = df_campanias["maniobra"].tolist()
    localizaciones = df_campanias["localizacion"].tolist()
    seriales = df_campanias["serial_boya"].tolist()
    
    texto = ""
    cantidad_maniobras = len(maniobras) 
    for it, (maniobra, localizacion, serial) in enumerate(zip(maniobras,localizaciones, seriales)):
        
        if "doris" in localizacion.lower():
            pass # Pendiente texto de las DORIS
        else:
            maniobra = maniobra.split(" ")[0]
            maniobra_str = crear_maniobra_str(maniobra)
                
            tipo = localizacion.split("-")[0]
            tipos_de_boyas[tipo]
            
            txt = f"{maniobra_str} de la {tipos_de_boyas[tipo]} con identificador {serial} correspondiente a la localización {localizacion}"
            if cantidad_maniobras == 1:
                texto += f"{txt}"
        
            elif cantidad_maniobras > 1:
                if it == cantidad_maniobras-1:
                    texto += f"y {txt}"
                else:
                    texto += f"{txt}, "
                
    return texto

def crear_conceptos(df_campanias: pd.DataFrame) -> str:
    
    df_campanias = df_campanias.drop_duplicates(subset=["localizacion"], keep="first")
    maniobras = df_campanias["maniobra"].tolist()
    localizaciones = df_campanias["localizacion"].tolist()
    
    texto= ""
    cantidad_maniobras = len(maniobras) 
    for it, (maniobra, localizacion) in enumerate(zip(maniobras,localizaciones)):
        
        if "BOT1" in localizacion.split("-")[0] and maniobra.lower() == "instalación":
            concepto = "1.1. Diseño del sistema de fijación, movilización e instalación de Boya Oceanográfica Tipo 1, y arranque de su sistema de adquisición y transmisión de datos oceanográficos"
        elif "BOT1" in localizacion.split("-")[0] and (maniobra.lower() == "recuperación" or maniobra.lower() == "búsqueda y rescate" or maniobra.lower() == "reinstalación" or "mantenimiento" in maniobra.lower()):
            concepto = "1.2 Mantenimiento de la Boya Oceanográfica Tipo 1, extracción y procesamiento de la información medida"
        elif "BOT1" in localizacion.split("-")[0] and maniobra.lower() == "retiro":
            concepto = "1.3 recuperación de la Boya Oceanográfica Tipo 1, extracción y procesamiento de la información medida"
        
        if "BOT2" in localizacion.split("-")[0] and maniobra.lower() == "instalación":
            concepto = "2.1. Diseño del sistema de fijación, movilización e instalación de Boya Oceanográfica Tipo 2, y arranque de su sistema de adquisición y transmisión de datos oceanográficos"
        elif "BOT2" in localizacion.split("-")[0] and (maniobra.lower() == "recuperación" or maniobra.lower() == "búsqueda y rescate" or maniobra.lower() == "reinstalación" or "mantenimiento" in maniobra.lower()):
            concepto = "2.2 Mantenimiento de la Boya Oceanográfica Tipo 2, extracción y procesamiento de la información medida"
        elif "BOT2" in localizacion.split("-")[0] and maniobra.lower() == "retiro":
            concepto = "2.3 recuperación de la Boya Oceanográfica Tipo 2, extracción y procesamiento de la información medida"
    
        if "BMT2" in localizacion.split("-")[0] and maniobra.lower() == "instalación":
            concepto = "3.1. Diseño del sistema de fijación, movilización e instalación de Boya Metoceánica Tipo 2, y arranque de su sistema de adquisición y transmisión de datos oceanográficos"
        elif "BMT2" in localizacion.split("-")[0] and (maniobra.lower() == "recuperación" or maniobra.lower() == "búsqueda y rescate" or maniobra.lower() == "reinstalación" or "mantenimiento" in maniobra.lower()):
            concepto = "3.2 Mantenimiento de la Boya Metoceánica Tipo 2, extracción y procesamiento de la información medida"
        elif "BMT2" in localizacion.split("-")[0] and maniobra.lower() == "retiro":
            concepto = "3.3 recuperación de la Boya Metoceánica Tipo 2, extracción y procesamiento de la información medida"
            
        if "BMT3" in localizacion.split("-")[0] and maniobra.lower() == "instalación":
            concepto = "4.1. Diseño del sistema de fijación, movilización e instalación de Boya Metoceánica Tipo 3, y arranque de su sistema de adquisición y transmisión de datos oceanográficos"
        elif "BMT3" in localizacion.split("-")[0] and (maniobra.lower() == "recuperación" or maniobra.lower() == "búsqueda y rescate" or maniobra.lower() == "reinstalación" or "mantenimiento" in maniobra.lower()):
            concepto = "4.2 Mantenimiento de la Boya Metoceánica Tipo 3, extracción y procesamiento de la información medida"
        elif "BMT3" in localizacion.split("-")[0] and maniobra.lower() == "retiro":
            concepto = "4.3 recuperación de la Boya Metoceánica Tipo 3, extracción y procesamiento de la información medida"
        
        if "doris" in localizacion.lower() and maniobra.lower() == "despliegue doris":
            concepto = "10.1 Protocolo de liberación de las sondas oceanográficas y transmisión de datos"
        if "doris" in localizacion.lower() and maniobra.lower() == "despliegue doris derrame":
            concepto = "10.2 Protocolo de liberación de sondas oceanográficas y transmisión de datos por evento de derrame de hidrocarburos"
        if cantidad_maniobras == 1:
            texto += f"{concepto}"
       
        elif cantidad_maniobras > 1:
            if it == cantidad_maniobras-1:
                texto += f"y {concepto}"
            else:
                texto += f"{concepto}, " 
                
    return texto    

def aux_pie_imagen(df_campanias: pd.DataFrame) -> str:
    """"
    Así mismo, se realizará <<maniobra>> de la <<tipo_boya>> instalada en la localización <<localizacion_1>>
    texto = "<<maniobra>> de la <<tipo_boya>> instalada en la localización <<localizacion_1>>"
    
    """
    localizaciones = df_campanias["localizacion"].tolist()
    cantidad_localizaciones = len(localizaciones) 

    if cantidad_localizaciones == 1:
            texto = f"la localización {localizaciones[0]}"
    else:
        texto = "las localizaciones "
        for it, localizacion in enumerate(localizaciones):
            if it == cantidad_localizaciones-1:
                texto += f"y {localizacion}."
            else:
                texto += f"{localizacion}, "
                 
    return texto

def aux_crear_titulo_tabla1(df_campanias: pd.DataFrame) -> str:
    localizaciones = df_campanias["localizacion"].unique().tolist()
    texto = f"la localización"
    if len(localizaciones)> 1:
        texto = f"las localizaciones"
    return texto
        

def crear_diccionario_del_df_excel_maestro() -> dict:
    """Crea un diccionario a partir de un DataFrame del excel maestro.

    Descripción:
        Esta función toma un DataFrame que contiene los datos del excel maestro
        y crea un diccionario donde las claves son los nombres de las columnas
        y los valores son listas con los datos correspondientes.

    Parámetros:
        df (pandas.DataFrame): El DataFrame del excel maestro.

    Retorna:
        dict: Un diccionario con los datos del DataFrame."""
    
    df_campanias = leer_excel(nombre_de_hoja="campanias", header=0)
    df_campanias = df_campanias[df_campanias["campania"].isin(get_hacer_planes())]
    
    # ordeno las maniobras realizadas por hora
    df_campanias["fecha_y_hora_de_plan"] = pd.to_datetime(df_campanias["fecha_y_hora_de_plan"], format="%d/%m/%Y %H:%M", utc=True)
    df_campanias.sort_values(by="fecha_y_hora_de_plan", inplace=True)
    df_campanias.reset_index(drop=True, inplace=True)
    
    df_coordinadores = leer_excel(nombre_de_hoja="coordinadores", header=0) 
    df_coordinador = df_coordinadores[df_coordinadores["nombre"].str.strip() == df_campanias["coordinador"].str.strip().iloc[0]].iloc[0]
    coordinador = df_coordinador["grado_academico"] + " " + df_coordinador["nombre"]
    
    # Diccionario de meses en español
    meses_esp = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 
                 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}
    
    try:
        fecha_salida = pd.to_datetime(df_campanias["fecha_hora_de_embarque"].iloc[0], format="%d/%m/%Y %H:%M", utc=True)
        fecha_salida_cst = fecha_salida.tz_convert('America/Mexico_City')
        fecha_salida_str = f"{fecha_salida_cst.day} de {meses_esp[fecha_salida_cst.month]} de {fecha_salida_cst.year}"
        hora_salida_cst = f"{fecha_salida_cst.hour:02d}:{fecha_salida_cst.minute:02d}"
    except Exception as e:
        fecha_salida_str = None
        hora_salida_cst = None
        fecha_salida_cst = None
    try:
        fecha_llegada = pd.to_datetime(df_campanias["fecha_de_desembarque"].iloc[0], format="%d/%m/%Y %H:%M", utc=True)
        fecha_llegada_cst = fecha_llegada.tz_convert('America/Mexico_City')
        fecha_llegada_str = f"{fecha_llegada_cst.day} de {meses_esp[fecha_llegada_cst.month]} de {fecha_llegada_cst.year}"
        hora_llegada_cst = f"{fecha_llegada_cst.hour:02d}:{fecha_llegada_cst.minute:02d}"
    except Exception as e:
        hora_llegada_cst = None
        fecha_llegada_cst = None
        
    datos_de_la_navegacion = obtener_coords_ordenadas_distancias_y_tiempos(campania=get_hacer_planes())
  
    output_dict = {
        "<<crucero>>": df_campanias["campania"].iloc[0],
        "<<coordinador>>": coordinador,
        "<<sitio_embarque>>": df_campanias["sitio_de_embarque"].iloc[0],
        "<<fecha_embarque>>": fecha_salida_str,
        "<<hora_embarque>>": hora_salida_cst,
        "<<sitio_desembarque>>": df_campanias["sitio_de_desembarque"].iloc[0],
        "<<fecha_desembarque>>": fecha_llegada_str,
        "<<hora_desembarque>>": hora_llegada_cst,
        "<<distancia_total_a_navegar>>": datos_de_la_navegacion["distancia_total_en_mn"],
        "<<tiempo_total_a_navegar>>": datos_de_la_navegacion["tiempo_total_en_horas"],
        "<<concepto>>": crear_conceptos(df_campanias),
        "<<texto_parrafo_1>>": aux_parrafo1(df_campanias),
        "<<texto_parrafo_2>>": aux_parrafo2(df_campanias, fecha_salida_str, hora_salida_cst),
        "<<titulo_tabla_1>>": aux_crear_titulo_tabla1(df_campanias),
        "<<tabla1>>": aux_crear_datos_para_tabla1(df_campanias),
        "<<fig_mapa_derrotero>>": None,
        "<<pie_de_imagen>>": aux_pie_imagen(df_campanias),
        "<<texto_parrafo_3>>":aux_parrafo3(df_campanias),
        "<<tabla2>>": aux_crear_datos_para_tabla2(df_campanias)  # Salida, Travesía para la maniobra de la localizacion, maniobra de la localizacion, travesía para la maniobra de la localizacion, travesía a pto de llegada, llegada al pto de llegada. 
    }
            
    return output_dict

