from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..core.security import (
    get_password_hash,
    verify_password,
    create_acess_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    # Verifica se já existe usuário com esse e-mail
    existing = (
        db.query(models.User)
        .filter(models.User.email == user_in.email)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já está em uso",
        )

    hashed_password = get_password_hash(user_in.password)

    db_user = models.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,
        city=user_in.city,
        state=user_in.state,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post(
    "/login",
    response_model=schemas.Token,
)
def login(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.email == credentials.email)
        .first()
    )
    if not user or not verify_password(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            staturs_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    acess_token = create_acess_token({"sub": str(user.id)})
    
    return {
        "access_token": acess_token,
        "token_type": "bearer",
    }