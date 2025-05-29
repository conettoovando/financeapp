from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models.categoria import Categoria
from database.finance import get_db
from models.movimiento import Movimiento
from schemas.user_schema import VerifyToken
from controllers.user_controller import verify_token

router = APIRouter()

@router.get("/gastos-por-categoria")
def gastos_por_categoria(
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(verify_token)
):
    resultados = (
        db.query(Categoria.nombre, func.sum(Movimiento.monto).label("total"))
        .join(Categoria)
        .filter(
            Movimiento.usuario_id == user.user_id,
            Movimiento.tipo_movimiento.has(tipo="Gasto")
        )
        .group_by(Categoria.nombre)
        .all()
    )

    print(resultados)


    return [{"categoria": categoria, "total": total} for categoria, total in resultados]