from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..deps import get_db, get_current_user
from .. import models

router = APIRouter(prefix="/animals", tags=["reactions"])

class ReactIn(BaseModel):
    kind: str  # LIKE | DISLIKE | SUPERLIKE

@router.post("/{animal_id}/react")
def react_toggle(
    animal_id: int,
    data: ReactIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    kind = data.kind.upper()
    if kind not in ("LIKE", "DISLIKE", "SUPERLIKE"):
        raise HTTPException(400, "kind inválido")

    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(404, "Animal não encontrado")

    existing = (
        db.query(models.AnimalReaction)
        .filter(models.AnimalReaction.user_id == current_user.id,
                models.AnimalReaction.animal_id == animal_id)
        .first()
    )

    if existing and existing.kind == kind:
        # ✅ toggle off
        db.delete(existing)
        db.commit()
        liked_by_me = False
    else:
        if existing:
            existing.kind = kind
        else:
            existing = models.AnimalReaction(
                user_id=current_user.id,
                animal_id=animal_id,
                kind=kind,
            )
            db.add(existing)
        db.commit()
        liked_by_me = (kind == "LIKE" or kind == "SUPERLIKE")  # superlike conta como like

    # ✅ conta likes = LIKE + SUPERLIKE
    like_count = (
        db.query(models.AnimalReaction)
        .filter(models.AnimalReaction.animal_id == animal_id,
                models.AnimalReaction.kind.in_(("LIKE", "SUPERLIKE")))
        .count()
    )

    return {
        "animal_id": animal_id,
        "like_count": like_count,
        "liked_by_me": liked_by_me,
        "my_kind": None if not existing or (existing and existing.kind == kind and not liked_by_me) else kind
    }
