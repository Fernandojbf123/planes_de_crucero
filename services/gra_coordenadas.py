import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

def get_coordedadas_del_texto(longitud, latitud, localizacion):
        lon_txt = longitud + 0.05
        lat_txt = latitud + 0.007
        
        if "nuevo campechito" in localizacion.lower():
            lon_txt = longitud-0.4
            lat_txt = latitud-0.05
        elif "sánchez" in localizacion.lower():
            lon_txt = longitud-0.4
            lat_txt = latitud-0.05
        elif "isla aguada" in localizacion.lower():
            lon_txt = longitud-0.4
            lat_txt = latitud-0.05
        
        return lon_txt, lat_txt

def graficar_coordenadas(axe, navegacion):
    
    latitudes_plan = navegacion["latitudes_plan"]
    longitudes_plan = navegacion["longitudes_plan"]
    localizaciones = navegacion["localizaciones"]
    seriales_sondas = navegacion["seriales"] 
    
    lat_embarque = latitudes_plan[0] # latitud del punto inicial/final (es el mismo punto)
    lon_embarque = longitudes_plan[0] # longitud del punto inicial/final (es el mismo punto)
    loc_embarque = localizaciones[0]
    
    lat_sondas = latitudes_plan[1:-1] # latitudes de las localizaciones (sin incluir el punto inicial/final)
    lon_sondas = longitudes_plan[1:-1] # longitudes de las localizaciones (sin incluir el punto inicial/final)
    loc_sondas = localizaciones[1:-1] 
    
    # acá debo obtener las localizaciones de las sondas que son únicos y sus índices para filtrar lat_sondas, lon_sondas y seriales_sondas
    # además creo un nuevo array de únicos ("loc_sondas") que contiene los nombres de las localizaciones si es una boya y el serial si es una doris
    vistos = set()
    indices_unicos = []
    for i, loc in enumerate(loc_sondas):
        if loc not in vistos or "doris" in loc.lower():
            vistos.add(loc)
            indices_unicos.append(i)

    lat_sondas = [lat_sondas[i] for i in indices_unicos]
    lon_sondas = [lon_sondas[i] for i in indices_unicos]
    seriales_sondas = [seriales_sondas[i] for i in indices_unicos]
    loc_sondas = [loc_sondas[i] for i in indices_unicos]

    lat_desembarque = latitudes_plan[-1] # latitud de desembarque
    lon_desembarque = longitudes_plan[-1] # longitud de desembarque
    loc_desembarque = localizaciones[-1] # nombres de las localizaciones 
    
    # Son 3 partes
    lon_txt_usadas = []
    lat_txt_usadas = []
    # 1. Graficar ruta (línea azul)
    plt.plot(navegacion["longitudes_plan"], navegacion["latitudes_plan"], color='blue', linewidth=2, transform=ccrs.PlateCarree(), zorder=9)
    
    # 2. Graficar puntos de las localizaciones (rojo) y etiquetas (solo boyas)
    # Colores para doris (evitar rojo y naranja)
    colores_doris = ['blue', 'green', 'purple', 'cyan', 'magenta', 'yellow', 'lime', 'teal', 'pink', 'gray']
    for it, (lon_sonda, lat_sonda, serial_sonda, loc_sonda) in enumerate(zip(lon_sondas, lat_sondas, seriales_sondas, loc_sondas)):
        
        # Si es una doris se usa label y colores; y el legend
        if "doris" in loc_sonda.lower(): 
            color = colores_doris[it]
            lon_sonda = lon_sonda # + 0.005 + np.random.rand() *  0.01 # Desplazar un poco la sonda para que sea visible
            lat_sonda = lat_sonda # + 0.005 + np.random.rand() * 0.01 # Desplazar un poco la sonda para que sea visible
            axe.scatter(lon_sonda, lat_sonda, c=color, edgecolors='black', linewidths=1, s=35, label=serial_sonda, transform=ccrs.PlateCarree(), zorder=10)
        
        else: # Si es una boya, NO se usa etiqueta; se usa texto en la figura y color rojo
            axe.scatter(lon_sonda, lat_sonda, c='red', edgecolors='black', linewidths=1, s=35, transform=ccrs.PlateCarree(), zorder=10)
            # obtengo la coordenada del del texto
            lon_txt, lat_txt = get_coordedadas_del_texto(lon_sonda, lat_sonda, serial_sonda)
            for lon_txt_usada, lat_txt_usada in zip(lon_txt_usadas, lat_txt_usadas):
                dif_lon = abs(lon_txt - lon_txt_usada)
                dif_lat = abs(lat_txt - lat_txt_usada)
                if dif_lon < 0.01 and dif_lat < 0.01: 
                    # si las coordendas del texto están muy cerca de otra etiqueta, las modifico para que no se sobrepongan
                    lon_txt = lon_txt - 0.2
                    lat_txt = lat_txt - 0.07
            plt.text(lon_txt, lat_txt, f"{loc_sonda}", fontsize=12, fontweight='bold', color='black', 
                    bbox=dict(facecolor='white', alpha=.3, edgecolor='none', pad=5),transform=ccrs.PlateCarree(), zorder=11)
            lon_txt_usadas.append(lon_txt)
            lat_txt_usadas.append(lat_txt)
        
    # 3. Graficar punto inicial / final(naranja) y etiqueta (nombre del puerto)
    axe.scatter([lon_embarque], [lat_embarque], c='orange', edgecolors='black', linewidths=1, s=35, transform=ccrs.PlateCarree(), zorder=10)
    lon_txt, lat_txt = get_coordedadas_del_texto(lon_embarque, lat_embarque, loc_embarque)
    plt.text(lon_txt, lat_txt, f"{loc_embarque}", fontsize=12, fontweight='bold', color='black', 
                bbox=dict(facecolor='white', alpha=.3, edgecolor='none', pad=5),transform=ccrs.PlateCarree(), zorder=11)
    
    if loc_embarque.lower() != loc_desembarque.lower():
        axe.scatter([lon_desembarque], [lat_desembarque], c='orange', edgecolors='black', linewidths=1, s=35, transform=ccrs.PlateCarree(), zorder=10)
        lon_txt, lat_txt = get_coordedadas_del_texto(lon_desembarque, lat_desembarque, loc_desembarque)
        plt.text(lon_txt, lat_txt, f"{loc_desembarque}", fontsize=12, fontweight='bold', color='black', 
                    bbox=dict(facecolor='white', alpha=.3, edgecolor='none', pad=5),transform=ccrs.PlateCarree(), zorder=11)
    
    # Mostrar leyenda solo para los scatter con label (boyas)
    handles, labels = axe.get_legend_handles_labels()
    pares = [(h, l) for h, l in zip(handles, labels) if l and not l.startswith("_")]
    unicos = {}
    for h, l in pares:
        if l not in unicos:
            unicos[l] = h
    if unicos:
        axe.legend(unicos.values(), unicos.keys(), loc='upper right', fontsize=10, framealpha=0.5)
    return axe
    
