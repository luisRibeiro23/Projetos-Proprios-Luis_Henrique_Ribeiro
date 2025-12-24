from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Optional
import os
import uuid
import shutil

from .. import models, schemas
from ..deps import get_db, get_current_user, get_current_user_optional

router = APIRouter(prefix="/animals", tags=["animals"])

UPLOAD_DIR = "static/animals"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=list[schemas.AnimalRead])
def list_animals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional),
):
    animals = db.query(models.Animal).all()

    likes = db.query(models.AnimalReaction.animal_id).filter(
        models.AnimalReaction.kind.in_(("LIKE", "SUPERLIKE"))
    ).all()

    like_count_map = {}
    for (aid,) in likes:
        like_count_map[aid] = like_count_map.get(aid, 0) + 1

    liked_by_me_set = set()
    if current_user:
        mine = db.query(models.AnimalReaction.animal_id).filter(
            models.AnimalReaction.user_id == current_user.id,
            models.AnimalReaction.kind.in_(("LIKE", "SUPERLIKE"))
        ).all()
        liked_by_me_set = {aid for (aid,) in mine}

    for a in animals:
        a.like_count = like_count_map.get(a.id, 0)
        a.liked_by_me = (a.id in liked_by_me_set)

    return animals


@router.get("/{animal_id}", response_model=schemas.AnimalRead)
def get_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional),
):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    # like_count
    like_count = db.query(models.AnimalReaction).filter(
        models.AnimalReaction.animal_id == animal_id,
        models.AnimalReaction.kind.in_(("LIKE", "SUPERLIKE"))
    ).count()

    # liked_by_me
    liked_by_me = False
    if current_user:
        liked_by_me = db.query(models.AnimalReaction).filter(
            models.AnimalReaction.animal_id == animal_id,
            models.AnimalReaction.user_id == current_user.id,
            models.AnimalReaction.kind.in_(("LIKE", "SUPERLIKE"))
        ).first() is not None

    animal.like_count = like_count
    animal.liked_by_me = liked_by_me
    return animal


@router.post("", response_model=schemas.AnimalRead, status_code=status.HTTP_201_CREATED)
def create_animal(
    name: str = Form(...),
    species: str = Form(...),
    size: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    age: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != schemas.UserRole.ONG:
        raise HTTPException(status_code=403, detail="Apenas ONG pode cadastrar animais")

    image_url = None
    if photo is not None:
        ext = os.path.splitext(photo.filename)[1].lower() or ".jpg"
        fname = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(UPLOAD_DIR, fname)
        with open(path, "wb") as f:
            shutil.copyfileobj(photo.file, f)
        image_url = f"/static/animals/{fname}"

    animal = models.Animal(
        name=name,
        species=species,
        age=age,
        city=city,
        state=state,
        description=description,
        size=size,
        available=True,
        owner_id=current_user.id,
        image_url=image_url,
    )

    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@router.patch("/{animal_id}", response_model=schemas.AnimalRead)
def update_animal(
    animal_id: int,
    animal_in: schemas.AnimalUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    if animal.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é dono deste animal")

    data = animal_in.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(animal, k, v)

    db.commit()
    db.refresh(animal)
    return animal


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    if animal.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é dono deste animal")

    db.delete(animal)
    db.commit()
    return None


@router.post("/{animal_id}/image", response_model=schemas.AnimalRead)
def upload_animal_image(
    animal_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    if animal.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é dono deste animal")

    os.makedirs("static/animals", exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    path = f"static/animals/{filename}"

    with open(path, "wb") as f:
        f.write(file.file.read())

    animal.image_url = f"/static/animals/{filename}"
    db.commit()
    db.refresh(animal)
    return animal
from typing import List


@router.post("/{animal_id}/photos", response_model=schemas.AnimalRead)
def upload_animal_photos(
    animal_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    if animal.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é dono deste animal")

    os.makedirs("static/animals", exist_ok=True)

    # próxima posição
    last_pos = (
        db.query(models.AnimalPhoto.position)
        .filter(models.AnimalPhoto.animal_id == animal_id)
        .order_by(models.AnimalPhoto.position.desc())
        .first()
    )
    pos = (last_pos[0] + 1) if last_pos else 0

    for f in files:
        ext = os.path.splitext(f.filename)[1].lower() or ".jpg"
        fname = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join("static/animals", fname)

        with open(path, "wb") as out:
            shutil.copyfileobj(f.file, out)

        url = f"/static/animals/{fname}"
        db.add(models.AnimalPhoto(animal_id=animal_id, url=url, position=pos))
        pos += 1

        # se ainda não tem foto principal, define a primeira enviada como principal
        if not animal.image_url:
            animal.image_url = url

    db.commit()
    db.refresh(animal)
    return animal
