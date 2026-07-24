from fastapi import FastAPI
from routers import status, category

# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

app = FastAPI(
    title="Sistema de Gestión Hotelera API",
    description="API RESTful modular para el control de hospedajes, reservas, habitaciones y autenticación.",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc UI
)


# ==========================================
# REGISTRO DE ROUTERS
# ==========================================
app.include_router(status.router)
app.include_router(category.router)


# ==========================================
# ENDPOINT DE PRUEBA / HEALTH CHECK
# ==========================================

@app.get("/", tags=["Health Check"])
def root():
    """Ruta raíz para verificar que el servidor está en ejecución."""
    return {
        "status": "online",
        "message": "API del Hotel funcionando correctamente",
        "version": "1.0.0"
    }