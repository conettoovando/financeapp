from fastapi import APIRouter
from .cuenta_routes import router as cuenta_router
from .movimientos_routes import router as movimientos_router

api_router = APIRouter()

api_router.include_router(cuenta_router, prefix="/cuentas", tags=["Cuentas"])
api_router.include_router(movimientos_router, prefix="/movimientos", tags=["Movimientos"])