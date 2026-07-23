from fastapi import FastAPI

# Importa aquí tus routers a medida que los necesites
# from src.routers import auth, category, lodging, payment_method, room, user

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
# REGISTRO DE ROUTERS (Descomentar según módulos creados)
# ==========================================

# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(category.router)
# app.include_router(room.router)
# app.include_router(payment_method.router)
# app.include_router(lodging.router)


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