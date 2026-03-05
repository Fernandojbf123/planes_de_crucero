import netCDF4 as nc
import numpy as np
from configs.manager_doc_config import *

def cargar_datos_de_batimetria() -> dict:
    """ Carga datos de batimetría desde un archivo NetCDF. Especificada en el archivo de configuración general.
    Salida
    
    datos_batimetria = {
        "lon": array_like,
        "lat": array_like,
        "elevation": array_like,
        "curvas_de_batimetria": array_like
    }
    
    """
    datos_batimetria = {
        "lon": None,
        "lat": None,
        "elevation": None,
        "curvas_de_batimetria": [-2000, -1000, -500, -100, -50, -20]
    }
    
    ruta = get_ruta_a_datos_batimetria()
        
    with nc.Dataset(ruta) as data:
        lon = data.variables['x'][:]
        lat = data.variables['y'][:]
        elevation = data.variables['z'][:,:]

        LON, LAT = np.meshgrid(lon, lat)   
    
        datos_batimetria["lon"] = LON
        datos_batimetria["lat"] = LAT
        datos_batimetria["elevation"] = elevation
    
    return datos_batimetria