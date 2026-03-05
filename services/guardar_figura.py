import os
from configs.manager_doc_config import get_ruta_a_carpeta_de_las_figuras


def guardar_figura(fig, nombre_archivo="mapa_navegacion.png", dpi=300):
    """Guarda la figura de matplotlib en la carpeta especificada en la configuración.
    
    Args:
        fig: La figura de matplotlib a guardar.
        nombre_archivo: El nombre del archivo a guardar (por defecto "mapa_navegacion.png").
        dpi: La resolución de la imagen (por defecto 300).
    
    Returns:
        str: La ruta completa donde se guardó la figura.
    """
    # Obtener la ruta de la carpeta de guardado
    carpeta_guardado = get_ruta_a_carpeta_de_las_figuras()
    
    # Crear la carpeta si no existe
    os.makedirs(carpeta_guardado, exist_ok=True)
    
    # Construir la ruta completa del archivo
    ruta_completa = os.path.join(carpeta_guardado, nombre_archivo)
    
    # Guardar la figura
    fig.savefig(ruta_completa, dpi=dpi, bbox_inches='tight')
    
    print(f"Figura guardada en: {ruta_completa}")
    
    return ruta_completa
