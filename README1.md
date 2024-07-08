# Guía para Ejecutar el Backend en el Servidor

# Ejecución de la Aplicación Backend

Esta guía proporciona los pasos necesarios para ejecutar tu aplicación backend en tu servidor utilizando Python y Flask.

## Requisitos Previos

- Python y pip instalados en tu servidor.
- Acceso SSH al servidor.
- Conocimientos básicos de línea de comandos.

## Paso 1: Preparar el Proyecto

1. **Clonar o Copiar el Proyecto:**
   Asegúrate de tener el código fuente del backend en tu servidor. Puedes clonarlo desde un repositorio remoto o copiar los archivos manualmente.

2. **Instalar Dependencias:**
   Crea y activa un entorno virtual (recomendado) y luego instala las dependencias del proyecto:
   ```bash
   python -m venv env       # Crea un entorno virtual (opcional)
   source env/bin/activate  # Activa el entorno virtual (si lo creaste)
   pip install -r requirements.txt  # Instala las dependencias
   ```

## Paso 2: Ejecutar el Backend

1. **Iniciar la Aplicación:**
   Usa nohup para iniciar tu aplicación Flask en segundo plano. Asegúrate de que esté escuchando en el puerto adecuado (por ejemplo, puerto 3333):
   ```bash
   nohup python index.py &
   ```

## Paso 3: Verificar la Aplicación

1. **Verificar el Estado de la Aplicación:**
   Puedes verificar que tu aplicación está corriendo correctamente con herramientas como ps o htop:

   ```bash
   ps aux | grep python # Verifica que el proceso de Python esté corriendo
   ```

2. **Ver los Logs de la Aplicación:**
   Si necesitas revisar logs específicos de tu aplicación, puedes hacerlo accediendo al archivo donde redirigiste la salida de nohup (por ejemplo, nohup.out).

## Paso 4: Acceder a tu Aplicación

Una vez que tu backend esté ejecutándose en el servidor, puedes acceder a él desde otras partes de tu aplicación frontend o realizar peticiones API utilizando la dirección IP o el dominio del servidor y el puerto especificado.

Ejemplo de URL:

```bash
http://mi-direccion-ip:3333/
```
