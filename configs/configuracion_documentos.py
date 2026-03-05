# 1. RUTAS
ruta_a_la_base_de_datos = "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\base_de_datos_general"
ruta_a_carpeta_de_las_figuras = "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\planes_de_crucero\\figuras"
ruta_a_carpeta_de_guardado_del_documento = "C:\\Users\\Atmosfera\\Desktop\\datos_procesados\\planes_de_crucero"
ruta_a_la_plantilla_de_word = "C:\\programacion\\codigos_python\\planes_de_crucero\\utils\\plantilla_plan_de_crucero.docx" # CAMBIAR A DISCRECIÓN (EL ARCHIVO VIENE INCLUIDO EN EL PROYECTO)
ruta_a_la_batimetria = "C:/programacion/codigos_python/bases_de_datos/topografia_ETOPO1_Ice_g_gmt4.nc"

usar_NAS = False # Indica si se quiere usar la ruta al NAS (True) o las rutas relativas (False). Si se usa el NAS, las rutas relativas se concatenarán a la ruta al NAS. Si no se usa el NAS, se usarán las rutas relativas tal cual están definidas.

velocidad_de_embarcacion = 15 # En nudos/hora.
hacer_planes = ["ASM-170"] 

### 2. Nombre de los estilos usados en la la plantilla
estilo_normal = "Normal"
estilo_texto_tablas_centrado = "texto_tablas_centrado"
estilo_texto_tablas_justificado = "texto_tablas_justificado"
estilo_pie_de_imagen = "Car"