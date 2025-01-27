# ******************** BACKEND *********************

## Para Ejecutarlo:
1. **Crea un entorno virtual:**
   ```
   python -m venv env
   ```

2. **Ingresa en el entorno virtual:**
   ```
   env\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```
   pip install -r requirements.txt
   ```

4. **Ejecuta el backend:**
   ```
   python index.py
   ```

---

## Para consumir datos descargados o usar datos en tiempo real:
En la carpeta `routes`, hay tres archivos principales que controlan cómo se consumen los datos:

- **`routes-json.py`:** Contiene datos descargados en formato JSON para trabajar con datos estáticos.
- **`routes-local.py`:** Configurado para usar datos en tiempo real directamente desde Scopus.
- **`routes-descarga.py`:** Permite usar datos en tiempo real y descargarlos también en un archivo JSON.

### Selección del archivo adecuado:
1. Ingresa al archivo correspondiente según lo que necesites.
2. Copia todo su contenido.
3. Pégalo en el archivo `routes.py`, que es el archivo principal con el que funciona el backend.

---

# ******************** CRUD DE INVESTIGADORES *********************

## Para ingresar al CRUD de los investigadores, sigue estos pasos:
1. **Accede a la carpeta correspondiente:**
   ```
   cd src/mongo-crud/
   ```

2. **Crea un entorno virtual:**
   ```
   python -m venv env
   ```

3. **Ingresa en el entorno virtual:**
   ```
   env\Scripts\activate
   ```

4. **Instala las dependencias:**
   ```
   pip install -r requirements.txt
   ```

5. **Ejecuta el CRUD:**
   ```
   python app.py
   ```

6. **Accede al CRUD:**
   Abre la siguiente URL en tu navegador:
   ```
   http://127.0.0.1:1000/