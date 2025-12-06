from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db

router = APIRouter(
    prefix="/animals",
    tags=["animals"],
    
)

@router.post(
    "",
    response_model=schemas.AnimalRead,
    status_code=status.HTTP_201_CREATED,
)
def create_animal(
    animal_in: schemas.AnimalCreate,
    db: Session = Depends(get_db),
):
    """
    Cadastra um novo animal para adoção.
    (por enquanto sem vincular a usuário/ONG; depois podemos atrelar ao usuário logado)
    """
    animal = models.Animal(
        name=animal_in.name,
        species=animal_in.species,
        size=animal_in.size,
        age=animal_in.age,
        description=animal_in.description,
        city=animal_in.city,
        state=animal_in.state,
        available=animal_in.available,
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@router.get(
    "",
    response_model=List[schemas.AnimalRead],
)
def list_animals(
    species: Optional[str] = Query(None, description="Filtrar por espécie, ex: cachorro, gato"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    state: Optional[str] = Query(None, description="Filtrar por UF"),
    only_available: bool = Query(True, description="Apenas animais disponíveis para adoção"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Lista animais com filtros simples.
    """
    query = db.query(models.Animal)

    if species:
        query = query.filter(models.Animal.species.ilike(f"%{species}%"))
    if city:
        query = query.filter(models.Animal.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(models.Animal.state == state)
    if only_available:
        query = query.filter(models.Animal.available == True)

    animals = query.offset(skip).limit(limit).all()
    return animals

@router.get(
    "/{animal_id}",
    response_model=schemas.AnimalRead,
)
def get_animal(
    animal_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um animal específico
    """
    # Pega de fato o objeto, não só o Query
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    # ou: animal = db.get(models.Animal, animal_id)

    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    return animal


@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_animal(
    animal_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove um animal do sistema
    """
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    # ou: animal = db.get(models.Animal, animal_id)

    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    db.delete(animal)
    db.commit()
    # 204 = sem corpo na resposta
    return None
