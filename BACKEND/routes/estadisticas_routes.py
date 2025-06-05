from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import func, literal_column, or_
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
    # Aliased para evitar confusiones en el join
    CategoriaAlias = aliased(Categoria)

    resultados = (
        db.query(
            Categoria.nombre,
            func.coalesce(func.sum(Movimiento.monto), 0).label("total")
        )
        .select_from(Categoria)
        .outerjoin(
            Movimiento,
            (Movimiento.categoria_id == Categoria.id) &
            (Movimiento.usuario_id == user.user_id) &
            (Movimiento.tipo_movimiento.has(tipo="Gasto"))
        )
        .filter(
            or_(
                Categoria.usuario_id == user.user_id,
                Categoria.usuario_id == None
            )
        )
        .group_by(Categoria.nombre)
        .order_by(Categoria.nombre)
        .all()
    )

    return [{"categoria": nombre, "total": float(total)} for nombre, total in resultados]