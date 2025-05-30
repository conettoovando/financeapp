from fastapi import APIRouter
from .cuenta_routes import router as cuenta_router
from .movimientos_routes import router as movimientos_router
from .categorias_routes import router as categoria_router
from .destinatarios_router import router as destinatarios_router
from .estadisticas_routes import router as estadisticas_router

api_router = APIRouter()

api_router.include_router(cuenta_router, prefix="/cuentas", tags=["Cuentas"])
api_router.include_router(movimientos_router, prefix="/movimientos", tags=["Movimientos"])
api_router.include_router(categoria_router, prefix="/categorias", tags=["Categorias"])
api_router.include_router(destinatarios_router, prefix="/destinatarios", tags=["Destinatarios"])
api_router.include_router(estadisticas_router, prefix="/estadisticas", tags=["Estadisticas"])