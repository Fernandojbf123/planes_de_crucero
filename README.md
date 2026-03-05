
# Proyecto Python: Planes de crucero

## Descripción del proyecto

Este proyecto carga datos históricos de un plan de crucero seleccionado en el archivo `configs/configuracion_documentos.py` y grafica el mapa con las coordenadas de los puntos a visitar, así como las trayectorias desde el puerto de salida. Calcula las distancias y los tiempos de viaje a cada localización. Por último, genera un reporte en formato Word con la información procesada.

En la carpeta `utils` se encuentra una demo de la plantilla utilizada para la generación del reporte.

## Requisitos

- Python 3.14.2 (la versión requerida está especificada en el archivo `runtime.txt`)
- Se recomienda el uso de un entorno virtual (venv)

## Instalación

1. **Clona el repositorio o descarga los archivos en tu máquina local.**

2. **Crea y activa un entorno virtual (opcional pero recomendado):**

   En Windows:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En Linux/MacOS:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**

   Ejecuta el siguiente comando para instalar todas las librerías necesarias:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará automáticamente todos los paquetes requeridos listados en el archivo `requirements.txt`.

4. **Verifica la versión de Python:**

   El archivo `runtime.txt` contiene la versión de Python recomendada para este proyecto. Asegúrate de estar usando la misma versión para evitar problemas de compatibilidad.

5. **Configura el archivo `.env`:**

   Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido de ejemplo:

   ```dotenv
   ruta_al_NAS = 
   lon_coe = 
   lat_coe = 
   ```
   
   - `ruta_al_NAS`: Ruta de red al almacenamiento NAS.
   - `lon_coe`: Longitud de la coordenada de referencia.
   - `lat_coe`: Latitud de la coordenada de referencia.

   Completa los valores de `lon_coe` y `lat_coe` según corresponda.

6. **Ejecuta el proyecto:**

   Puedes ejecutar los scripts principales, por ejemplo:
   ```bash
   python main_despliegue.py
   ```

## Notas adicionales

- Asegúrate de tener acceso a la ruta de red especificada en `ruta_al_NAS`.
- Si tienes problemas con dependencias, revisa el archivo `requirements.txt`.

---

**Ejemplo de archivo `.env`:**

```dotenv
ruta_al_NAS = 
lon_coe = 
lat_coe = 
```
