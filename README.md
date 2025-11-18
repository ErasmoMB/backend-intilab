# Backend - Slider Scopus

Backend escalable con FastAPI para la gestión de investigadores y datos de Scopus.

## Estructura del Proyecto

```
backend/
├── .env                    # Variables de entorno (NO en git)
├── .env.example            # Template de variables
├── config.py               # Configuración legacy (compatibilidad)
├── main.py                 # Punto de entrada
├── requirements.txt
├── src/
│   ├── config/
│   │   ├── settings.py      # Configuración centralizada
│   │   ├── database.py      # MongoDB compartido
│   │   └── s3.py           # S3 compartido
│   ├── models/
│   │   ├── author.py
│   │   ├── document.py
│   │   └── investigador.py
│   ├── services/
│   │   ├── scopus_service.py
│   │   ├── s3_service.py
│   │   └── investigador_service.py
│   ├── routes/
│   │   ├── routes.py
│   │   └── api/
│   │       ├── public/      # Rutas públicas
│   │       │   ├── authors.py
│   │       │   └── documents.py
│   │       └── admin/        # Rutas protegidas
│   │           └── investigadores.py
│   ├── middleware/
│   │   └── auth.py          # Autenticación
│   ├── utils/
│   │   ├── exceptions.py
│   │   ├── validators.py
│   │   └── logger.py
│   └── test/
│       ├── test_routes.py
│       └── test_services.py
```

## Configuración Inicial

### 1. Crear archivo .env

Copia `.env.example` a `.env` y completa las variables:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
SCOPUS_API_KEY=tu_api_key_de_scopus
AWS_ACCESS_KEY_ID=tu_aws_access_key
AWS_SECRET_ACCESS_KEY=tu_aws_secret_key
S3_BUCKET=se-autores
S3_REGION=us-east-1
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/database
MONGODB_DB_NAME=InvestigadoresUch
MONGODB_COLLECTION=investigadores
FLASK_ENV=development
PORT=5000
SECRET_KEY=tu_secret_key_seguro
CORS_ORIGINS=http://localhost:3000
```

### 2. Instalar dependencias

```bash
cd backend
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Ejecutar el backend

```bash
python main.py
```

O con uvicorn directamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

El servidor se ejecutará en `http://0.0.0.0:5000`

**Documentación automática:**
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## API Endpoints

### Rutas Públicas

#### Autores
- `GET /api/public/authors` - Obtener todos los autores
- `GET /api/public/authors/ids?ids=id1&ids=id2` - Obtener autores por IDs
- `GET /api/public/authors/uch` - Obtener autores UCH

#### Documentos
- `GET /api/public/documents` - Obtener documentos
- `GET /api/public/documents?au_id=id` - Obtener documentos por autor
- `GET /api/public/documents/ciics` - Documentos CIICS
- `GET /api/public/documents/e-health` - Documentos E-Health
- `GET /api/public/documents/inti-lab` - Documentos Inti-Lab
- `GET /api/public/documents/uch` - Información UCH

### Rutas de Administración (Protegidas)

Todas las rutas de administración requieren autenticación mediante header:

```
Authorization: Bearer <SECRET_KEY>
```

#### Investigadores
- `GET /api/admin/investigadores` - Listar investigadores
- `GET /api/admin/investigadores/<id>` - Obtener investigador por ID
- `POST /api/admin/investigadores` - Crear investigador
- `PUT /api/admin/investigadores/<id>` - Actualizar investigador
- `DELETE /api/admin/investigadores/<id>` - Eliminar investigador

### Otras Rutas
- `GET /datos` - Obtener datos de investigadores (público)
- `GET /health` - Health check

## Características

- ✅ Arquitectura escalable y modular
- ✅ Separación de responsabilidades (servicios, modelos, rutas)
- ✅ Manejo centralizado de errores
- ✅ Logging estructurado
- ✅ Validación de datos
- ✅ Autenticación para rutas admin
- ✅ Variables de entorno para configuración
- ✅ CORS configurado
- ✅ Conexión a MongoDB con pooling
- ✅ Integración con AWS S3
- ✅ Código limpio sin comentarios innecesarios

## Buenas Prácticas Implementadas

1. **Configuración**: Variables de entorno para credenciales
2. **Logging**: Sistema de logs con rotación
3. **Errores**: Manejo centralizado de excepciones
4. **Validación**: Validadores para datos de entrada
5. **Servicios**: Lógica de negocio separada de las rutas
6. **Modelos**: Modelos de datos estructurados
7. **Seguridad**: Autenticación en rutas admin
8. **Escalabilidad**: Estructura modular fácil de extender

## Desarrollo

### Ejecutar en modo desarrollo

```bash
python main.py
```

O con uvicorn con reload:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Ejecutar en producción

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

## Testing

```bash
python -m pytest src/test/
```

## Notas

- El CRUD de investigadores está integrado en el backend principal
- Las credenciales deben estar en `.env` (nunca en el código)
- El archivo `.env` está en `.gitignore` por seguridad
