from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.settings import config
from src.config.database import db
from src.utils.logger import logger
from src.routes.routes import router as routes_router
from src.routes.api.scopus.authors import router as scopus_authors_router
from src.routes.api.scopus.documents import router as scopus_documents_router
from src.routes.api.datos.authors import router as datos_authors_router
from src.routes.api.datos.documents import router as datos_documents_router
from src.routes.api.datos.investigadores import router as datos_investigadores_router
from src.routes.api.public.institucion import router as public_institucion_router
from src.routes.api.admin.investigadores import router as investigadores_router
from src.routes.api.admin.institucion import router as institucion_router
from src.routes.api.admin.cache import router as cache_router
from src.routes.api.auth.login import router as auth_router

ROUTERS = [
    routes_router,
    scopus_authors_router,
    scopus_documents_router,
    datos_authors_router,
    datos_documents_router,
    datos_investigadores_router,
    public_institucion_router,
    investigadores_router,
    institucion_router,
    cache_router,
    auth_router,
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db.connect()
        from src.services.institucion_service import institucion_service
        institucion_service.obtener_configuracion()
        logger.info("Aplicación iniciada correctamente")
    except Exception as e:
        logger.warning(f"Error al inicializar base de datos: {e}")
        logger.warning("El backend continuará sin conexión a MongoDB")
    yield
    db.close()
    logger.info("Aplicación cerrada correctamente")

app = FastAPI(
    title="Slider Scopus API",
    description="API para gestión de investigadores y datos de Scopus",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ROUTERS:
    app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=(config.FLASK_ENV == 'development')
    )
