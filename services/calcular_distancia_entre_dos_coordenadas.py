import numpy as np

def calcular_distancia_entre_dos_coordenadas(lon_fin, lat_fin, lon_ini, lat_ini, velocidad_nudos):
    distancia_deg = np.sqrt((lon_ini - lon_fin)**2 + (lat_ini - lat_fin)**2)
    distancia_km = distancia_deg * 111.32
    distancia_mn = distancia_km / 1.852
    tiempo_h = distancia_mn / velocidad_nudos
    tiempo_redondeado = round(tiempo_h * 2) / 2
    salida = {
        "distancia_km": distancia_km,
        "distancia_mn": distancia_mn,
        "tiempo_h": tiempo_h,
        "tiempo_redondeado": tiempo_redondeado
    }
    return salida