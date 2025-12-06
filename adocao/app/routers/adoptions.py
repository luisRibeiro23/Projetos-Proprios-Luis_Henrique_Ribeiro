from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db

router = APIRouter(
    prefix="/adoption-requests",
    tags=["adoption-requests"],
)

@router.post(
    "",
    response_model=schemas.AdoptionRequestRead,
    status_code=status.HTTP_201_CREATED,
)
def create_adoption_request(
    adoption_in: schemas.AdoptionRequestCreate,
    db: Session = Depends(get_db),
):
    """
    Cria uma nova solicitação de adoção.
    (Versão simples: recebe user_id no body.)
    """
    animal = db.query(models.Animal).filter(models.Animal.id == adoption_in.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    if not animal.available:
        raise HTTPException(status_code=400, detail="Animal não está disponível para adoção")

    user = db.query(models.User).filter(models.User.id == adoption_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    adoption_request = models.AdoptionRequest(
        user_id=adoption_in.user_id,
        animal_id=adoption_in.animal_id,
        message=adoption_in.message,
        # status usa o default PENDENTE do model
    )

    db.add(adoption_request)
    db.commit()
    db.refresh(adoption_request)
    return adoption_request


@router.get(
    "",
    response_model=List[schemas.AdoptionRequestRead],
)
def list_adoption_requests(
    status_filter: Optional[schemas.AdoptionStatus] = Query(
        None,
        description="Filtrar por status: PENDENTE, APROVADO, RECUSADO"
    ),
    user_id: Optional[int] = Query(None, description="Filtrar por id do usuário"),
    animal_id: Optional[int] = Query(None, description="Filtrar por id do animal"),
    db: Session = Depends(get_db),
):
    """
    Lista solicitações de adoção com filtros simples.
    """
    query = db.query(models.AdoptionRequest)

    if status_filter:
        query = query.filter(models.AdoptionRequest.status == status_filter.value)
    if user_id:
        query = query.filter(models.AdoptionRequest.user_id == user_id)
    if animal_id:
        query = query.filter(models.AdoptionRequest.animal_id == animal_id)

    return query.all()


@router.get(
    "/{request_id}",
    response_model=schemas.AdoptionRequestRead,
)
def get_adoption_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    """
    Retorna detalhes de uma solicitação específica.
    """
    adoption_request = db.query(models.AdoptionRequest).filter(
        models.AdoptionRequest.id == request_id
    ).first()

    if not adoption_request:
        raise HTTPException(status_code=404, detail="Solicitação de adoção não encontrada")

    return adoption_request


@router.patch(
    "/{request_id}/status",
    response_model=schemas.AdoptionRequestRead,
)
def update_adoption_request_status(
    request_id: int,
    status_in: schemas.AdoptionRequestUpdateStatus,
    db: Session = Depends(get_db),
):
    """
    Atualiza o status de uma solicitação de adoção.

    Regra:
    - Se status == APROVADO, animal.available = False
    - Se status == RECUSADO, animal.available = True (se for essa a regra)
    """
    adoption_request = db.query(models.AdoptionRequest).filter(
        models.AdoptionRequest.id == request_id
    ).first()

    if not adoption_request:
        raise HTTPException(status_code=404, detail="Solicitação de adoção não encontrada")

    animal = adoption_request.animal
    if not animal:
        raise HTTPException(status_code=500, detail="Animal associado não encontrado")

    # status_in.status é um Enum -> grava o valor string ("PENDENTE", "APROVADO", "RECUSADO")
    adoption_request.status = status_in.status.value

    if status_in.status == schemas.AdoptionStatus.APROVADO:
        animal.available = False
    elif status_in.status == schemas.AdoptionStatus.RECUSADO:
        animal.available = True
    # PENDENTE: não mexemos em available

    db.commit()
    db.refresh(adoption_request)
    return adoption_request
