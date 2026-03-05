import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import numpy as np

def dar_formato_al_mapa(propieadades_de_mapa = None) -> None:
    """
    Descripción:
        Aplica formato completo a un mapa creado con matplotlib/cartopy.
        Configura títulos, etiquetas de ejes, grid, tamaños de fuente y barra de color
        (colorbar) si se proporciona un objeto mapeable.

    Parámetros:
        propieadades_de_mapa (dict): Diccionario con las propiedades del mapa a formatear.
            - "obj_axes" (matplotlib.axes.Axes): Objeto axis de matplotlib (requerido).
            - "titulo" (str, opcional): Título principal del mapa. Por defecto: ''.
            - "subtitulo" (str, opcional): Subtítulo del mapa. Por defecto: ''.
            - "ylabel" (str, opcional): Etiqueta del eje Y (latitud). Por defecto: ''.
            - "xlabel" (str, opcional): Etiqueta del eje X (longitud). Por defecto: ''.
            - "grid" (bool, opcional): Si True, muestra grid en el mapa. Por defecto: True.
            - "obj_mapeable" (PathCollection o None, opcional): Objeto scatter para colorbar. Por defecto: None.
            - "colorbar_label" (str, opcional): Etiqueta de la barra de color. Por defecto: ''.
            - "colorbar_min" (float, opcional): Valor mínimo de la barra de color. Por defecto: 0.
            - "colorbar_max" (float, opcional): Valor máximo de la barra de color. Por defecto: 1.5.

    Retorna:
        None: Modifica el objeto Axes y la figura directamente (in-place).

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fig, ax = plt.subplots()
        >>> x = np.random.rand(50) * 10 - 75  # longitudes
        >>> y = np.random.rand(50) * 5 + 35   # latitudes
        >>> valores = np.random.rand(50) * 2.5  # altura de ola
        >>> scatter = ax.scatter(x, y, c=valores, cmap='viridis', vmin=0, vmax=2.5)
        >>> propiedades = {
        ...     "obj_axes": ax,
        ...     "titulo": "Mapa de Altura de Ola",
        ...     "subtitulo": "Región del Pacífico",
        ...     "xlabel": "Longitud (°)",
        ...     "ylabel": "Latitud (°)",
        ...     "grid": True,
        ...     "obj_mapeable": scatter,
        ...     "colorbar_label": "Hs (m)",
        ...     "colorbar_min": 0,
        ...     "colorbar_max": 2.5
        ... }
        >>> dar_formato_al_mapa(propiedades)
        >>> plt.show()

    Notas:
        - Si se proporciona tanto título como subtítulo, se muestran en dos líneas.
        - La barra de color solo se crea si obj_mapeable no es None.
        - Los tamaños y tipos de fuente se obtienen de funciones de configuración.
        
    Funciones auxiliares:
        - get_tipo_letra(): Obtiene el tipo de fuente configurado
        - get_tamanio_de_letra(): Obtiene el tamaño base de fuente
        - get_decimales_figuras(): Obtiene decimales para ticks del colorbar
        
    Categoría:
        Gráficos
    """
    # Extraer propiedades con valores por defecto si no se proporcionan
    obj_axes = propieadades_de_mapa.get("obj_axes", None)
    titulo = propieadades_de_mapa.get("titulo", '') 
    subtitulo = propieadades_de_mapa.get("subtitulo", '') 
    ylabel = propieadades_de_mapa.get("ylabel", '') 
    xlabel = propieadades_de_mapa.get("xlabel", '') 
    grid = propieadades_de_mapa.get("grid", True) 
    obj_mapeable = propieadades_de_mapa.get("obj_mapeable", None) 
    colorbar_label = propieadades_de_mapa.get("colorbar_label", '') 
    minimo = propieadades_de_mapa.get("colorbar_min", 0) 
    maximo = propieadades_de_mapa.get("colorbar_max", 1.5) 
    
    tipo_de_letra = "Microsoft Sans Serif" # fontfamily
    tamanio_de_letra = 10
    title_size = tamanio_de_letra + 4
    xlabelsize = tamanio_de_letra + 2
    ylabelsize = tamanio_de_letra + 2
    yticksize = tamanio_de_letra + 2
    xticksize = tamanio_de_letra + 2
    colorbar_labelsize = tamanio_de_letra + 2
    colorbar_ticksize = tamanio_de_letra + 1
    
    if obj_axes is None:
        raise ValueError("Debes indicar a qué axis se le pondrán las propiedades.")
    
    ## Titulos
    plt.title(titulo, font=tipo_de_letra, fontweight='bold', fontsize=title_size, pad = 10)
    if titulo and subtitulo:
        plt.title(titulo + "\n" + subtitulo, font=tipo_de_letra, fontweight='bold', fontsize=title_size, pad = 20)
    
    # xlabel y ylabel con tipo y tamaño de letra
    obj_axes.set_xlabel(xlabel, fontname=tipo_de_letra, fontweight='bold', fontsize=xlabelsize)
    obj_axes.set_ylabel(ylabel, fontname=tipo_de_letra, fontweight='bold', fontsize=ylabelsize)
    
    # Ejes: tamaño y tipo de letra de los ticks X y Y
    for label in obj_axes.get_xticklabels():
        label.set_fontname(tipo_de_letra)
        label.set_fontsize(xticksize)
    for label in obj_axes.get_yticklabels():
        label.set_fontname(tipo_de_letra)
        label.set_fontsize(yticksize)
    
    # Grid (usando gridlines de cartopy para proyecciones)
    if grid:
        # Obtener los ticks actuales del axes
        xticks = obj_axes.get_xticks()
        yticks = obj_axes.get_yticks()
        
        # Obtener los límites del mapa
        xlim = obj_axes.get_xlim()
        ylim = obj_axes.get_ylim()
        
        # Dibujar líneas verticales (longitudes)
        for x in xticks:
            obj_axes.plot([x, x], [ylim[0], ylim[1]], '--', color='gray', 
                         alpha=0.7, linewidth=0.8, zorder=15, transform=ccrs.PlateCarree())
        
        # Dibujar líneas horizontales (latitudes)
        for y in yticks:
            obj_axes.plot([xlim[0], xlim[1]], [y, y], '--', color='gray', 
                         alpha=0.7, linewidth=0.8, zorder=15, transform=ccrs.PlateCarree())
    
    # Agregar bordes negros al mapa
    for spine in obj_axes.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2.5)
    
    if obj_mapeable is not None:
        cb = plt.colorbar(obj_mapeable, label=colorbar_label, orientation='vertical', pad=0.02, aspect=30, ticks=np.round(np.linspace(minimo, maximo, 7), get_decimales_figuras()))
        cb.set_label(colorbar_label, fontname=tipo_de_letra, fontsize=colorbar_labelsize, fontweight='bold')
        # Ajustar tamaño y tipo de letra de los ticks del colorbar
        for label in cb.ax.get_yticklabels():
            label.set_fontname(tipo_de_letra)
            label.set_fontsize(colorbar_ticksize)
    
    plt.tight_layout()