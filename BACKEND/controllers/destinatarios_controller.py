from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.destinatario import Destinatario
from schemas.destinatarios_schema import CreateDestModel
from sqlalchemy import select

def obtener_destinataios(
        db: Session,
        user_id: str
):
    destinatarios = db.execute(
        select(Destinatario)
        .filter((Destinatario.usuario_id == user_id))
    ).scalars().all()

    return destinatarios

def crear_destinatario(
        db: Session, 
        user_id: str,
        data: CreateDestModel
):
    existe = db.execute(
        select(Destinatario)
        .filter(
            (Destinatario.usuario_id == user_id) &
            (Destinatario.nombre == data.nombre)
        )
    ).scalar_one_or_none()

    if existe:
        raise HTTPException(status_code=409, detail="Destinatario ya registrado")

    destinatario = Destinatario(
        usuario_id = user_id,
        nombre = data.nombre
    )

    db.add(destinatario)
    db.commit()
    db.refresh(destinatario)

    return destinatario

def actualizar_destinatario(
        db: Session,
        user_id: str,
        dest_id: str,
        data: CreateDestModel
):
    destinatario = db.get(Destinatario, dest_id)

    if destinatario is None:
        raise HTTPException(status_code=404, detail="Destinatario no registrado")
    
    if str(destinatario.usuario_id) != user_id:
        raise HTTPException(status_code=401, detail="Acceso no consedido")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(destinatario, key, value)

    db.commit()
    db.refresh(destinatario)

    return destinatario

def eliminar_destinatario(
        db: Session,
        user_id: str,
        dest_id
):
    dest_a_eliminar = db.get(Destinatario, dest_id)

    if not dest_a_eliminar:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado")
    
    if str(dest_a_eliminar.usuario_id) != user_id:
        raise HTTPException(status_code=401, detail="Acceso no consedido")

    db.delete(dest_a_eliminar)
    db.commit()

    return {"message": "Destinatario eliminado correctamente"}