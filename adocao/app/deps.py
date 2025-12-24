from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .db import SessionLocal
from . import models
from .core.config import settings


# URL do login que devolve o token (bate com o router auth)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    Dependência de sessão com o banco.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Decodifica o JWT, obtém o user_id do token e retorna o usuário do banco.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # o token deve ter sido criado com SECRET_KEY e ALGORITHM do settings
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        # aqui assumimos que `sub` é o ID do usuário
        user_id = int(sub)

    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[models.User]:
    """
    Retorna o usuário logado se existir token válido.
    Se não existir token (usuário anônimo), retorna None.
    """
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            return None
    except Exception:
        return None

    return db.query(models.User).filter(models.User.id == int(user_id)).first()