from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config.settings import config
from src.config.database import db
from src.routes.routes import router as routes_router
from src.routes.api.scopus.authors import router as scopus_authors_router
from src.routes.api.scopus.documents import router as scopus_documents_router
from src.routes.api.datos.authors import router as datos_authors_router
from src.routes.api.datos.documents import router as datos_documents_router
from src.routes.api.datos.investigadores import router as datos_investigadores_router
from src.routes.api.admin.investigadores import router as investigadores_router
from src.routes.api.admin.cache import router as cache_router
from src.utils.exceptions import APIException
from src.utils.logger import logger

app = FastAPI(
    title="Slider Scopus API",
    description="API para gestión de investigadores y datos de Scopus",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_router)
app.include_router(scopus_authors_router)
app.include_router(scopus_documents_router)
app.include_router(datos_authors_router)
app.include_router(datos_documents_router)
app.include_router(datos_investigadores_router)
app.include_router(investigadores_router)
app.include_router(cache_router)


@app.on_event("startup")
async def startup_event():
    try:
        db.connect()
    except Exception as e:
        logger.warning(f"Error al inicializar base de datos: {e}")
        logger.warning("El backend continuará sin conexión a MongoDB. Algunas funcionalidades pueden no estar disponibles.")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=(config.FLASK_ENV == 'development')
    )
