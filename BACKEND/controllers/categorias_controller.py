import requests
import jwt
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.categoria import Categoria
from schemas.categoria_schema import CreateCategoryModel
from sqlalchemy import func, select

def obtener_categorias(db: Session, user_id: str):
    categorias = db.execute(
        select(Categoria)
        .filter((Categoria.usuario_id == None) | (Categoria.usuario_id == user_id))
    ).scalars().all()

    if not categorias:
        raise HTTPException(status_code=500, detail="Error al obtener categorias")
    
    return categorias

def normalizar(texto: str) -> str:
    return "".join(texto.lower().split())

def crear_categoria(db: Session, user_id: str, model: CreateCategoryModel):
    nombre_normalizado = normalizar(model.nombre)

    existe = db.execute(
        select(Categoria)
        .filter(
            (func.replace(func.lower(Categoria.nombre), " ", "") == nombre_normalizado),
            (Categoria.usuario_id == None) | (Categoria.usuario_id == user_id) 
        )
    ).first()

    if existe:
        raise HTTPException(status_code=405, detail="Categoría creada previamente")
        
    nueva_categoria = Categoria(
        nombre=model.nombre.strip(),
        usuario_id=user_id
    )

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria

def actualizar_categoria(db: Session, user_id: str, model: CreateCategoryModel, id_cat: str):
    categoria = db.get(Categoria, id_cat)

    if categoria is None or str(categoria.usuario_id) != user_id:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    for campo, valor in model.model_dump(exclude_unset=True).items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)

    return categoria

def eliminar_categoria(db: Session, user_id: str, id_cat: str):
    categoria = db.get(Categoria, id_cat)

    if categoria is None or str(categoria.usuario_id) != user_id:
        raise HTTPException(status_code=404, detail="Categoria no encontrada o no autorizada")
    
    db.delete(categoria)
    db.commit()

    return {"message": "categoria eliminara con exito"}