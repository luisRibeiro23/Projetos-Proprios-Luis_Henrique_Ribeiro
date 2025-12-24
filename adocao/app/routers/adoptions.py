from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from ..db import SessionLocal
from .. import models
from .auth import get_current_user  # ajuste se seu import for diferente

router = APIRouter(prefix="/adoption-requests", tags=["Adoption Requests"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AdoptionRequestCreate(BaseModel):
    animal_id: int
    message: Optional[str] = None


class AdoptionRequestUpdate(BaseModel):
    status: str  # "APROVADO" | "REJEITADO" | "PENDENTE"


class AdoptionRequestOut(BaseModel):
    id: int
    status: str
    message: Optional[str] = None
    user_id: int
    animal_id: int

    class Config:
        from_attributes = True


VALID_STATUS = {"PENDENTE", "APROVADO", "REJEITADO"}


@router.post("", response_model=AdoptionRequestOut, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: AdoptionRequestCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "ADOTANTE":
        raise HTTPException(status_code=403, detail="Apenas ADOTANTE pode solicitar adoção.")

    animal = db.query(models.Animal).filter(models.Animal.id == payload.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado.")

    if not animal.available:
        raise HTTPException(status_code=400, detail="Animal indisponível para adoção.")

    # Impedir duplicata pendente do mesmo usuário pro mesmo animal
    existing = (
        db.query(models.AdoptionRequest)
        .filter(
            models.AdoptionRequest.animal_id == payload.animal_id,
            models.AdoptionRequest.user_id == user.id,
            models.AdoptionRequest.status == "PENDENTE",
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Você já tem uma solicitação pendente para este animal.")

    req = models.AdoptionRequest(
        animal_id=payload.animal_id,
        user_id=user.id,
        status="PENDENTE",
        message=payload.message,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.get("", response_model=List[AdoptionRequestOut])
def list_requests(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ADOTANTE: listar as próprias solicitações
    if user.role == "ADOTANTE":
        return (
            db.query(models.AdoptionRequest)
            .filter(models.AdoptionRequest.user_id == user.id)
            .order_by(models.AdoptionRequest.id.desc())
            .all()
        )

    # ONG: listar solicitações dos animais cadastrados por ela (Animal.owner_id)
    if user.role == "ONG":
        return (
            db.query(models.AdoptionRequest)
            .join(models.Animal, models.Animal.id == models.AdoptionRequest.animal_id)
            .filter(models.Animal.owner_id == user.id)
            .order_by(models.AdoptionRequest.id.desc())
            .all()
        )

    # DOADOR / outros
    return []


@router.patch("/{request_id}", response_model=AdoptionRequestOut)
def update_request_status(
    request_id: int,
    payload: AdoptionRequestUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "ONG":
        raise HTTPException(status_code=403, detail="Apenas ONG pode aprovar/rejeitar solicitações.")

    new_status = (payload.status or "").upper().strip()
    if new_status not in VALID_STATUS:
        raise HTTPException(status_code=400, detail=f"Status inválido: {new_status}")

    req = db.query(models.AdoptionRequest).filter(models.AdoptionRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    animal = db.query(models.Animal).filter(models.Animal.id == req.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal relacionado não encontrado.")

    # garantir que é a ONG dona do animal
    if animal.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para este animal.")

    req.status = new_status

    # Se aprovou, marca animal como indisponível
    if new_status == "APROVADO":
        animal.available = False

        # opcional: rejeitar automaticamente outras pendentes do mesmo animal
        db.query(models.AdoptionRequest).filter(
            models.AdoptionRequest.animal_id == req.animal_id,
            models.AdoptionRequest.id != req.id,
            models.AdoptionRequest.status == "PENDENTE",
        ).update({"status": "REJEITADO"})

    db.commit()
    db.refresh(req)
    return req
