from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


# =========================
# Enums
# =========================
class UserRole(str, Enum):
    ADOTANTE = "ADOTANTE"
    ONG = "ONG"
    DOADOR = "DOADOR"


class AdoptionStatus(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"  # ✅ mantenha assim (e ajuste o front p/ usar RECUSADO)


# =========================
# Auth / Users
# =========================
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# Animals
# =========================
class AnimalBase(BaseModel):
    name: str
    species: str

    # age como string porque no teu DB tem valores tipo "2 meses", "3 anos"
    age: Optional[str] = None

    city: str
    state: str
    description: Optional[str] = None

    # ✅ No seu models.py: size é nullable=False, então aqui deve ser obrigatório
    size: str

    available: Optional[bool] = True

    # ✅ NOVO: URL da imagem principal do animal
    image_url: Optional[str] = None


def _age_is_negative(age_str: str) -> bool:
    """
    Regras simples:
    - se começar com número, valida se é negativo
    - exemplos aceitos: "2", "2 anos", "2 meses", "0.5 anos"
    - se não começar com número, não valida (deixa passar como texto)
    """
    s = age_str.strip().lower()
    if not s:
        return False

    token = ""
    for ch in s:
        if ch.isdigit() or ch in "-.":
            token += ch
        else:
            break

    if token in ("", "-", ".", "-."):
        return False

    try:
        return float(token) < 0
    except Exception:
        return False


class AnimalCreate(AnimalBase):
    @field_validator("age")
    @classmethod
    def age_non_negative(cls, v):
        if v is None:
            return v
        if _age_is_negative(v):
            raise ValueError("Idade não pode ser negativa")
        return v

    @field_validator("state")
    @classmethod
    def state_two_letters(cls, v):
        v = v.strip().upper()
        if len(v) != 2:
            raise ValueError("UF deve ter 2 letras (ex: AM)")
        return v


class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    age: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    size: Optional[str] = None
    available: Optional[bool] = None

    # ✅ permitir atualizar foto também (ex: quando editar animal)
    image_url: Optional[str] = None

    @field_validator("age")
    @classmethod
    def age_non_negative(cls, v):
        if v is None:
            return v
        if _age_is_negative(v):
            raise ValueError("Idade não pode ser negativa")
        return v

    @field_validator("state")
    @classmethod
    def state_two_letters(cls, v):
        if v is None:
            return v
        v = v.strip().upper()
        if len(v) != 2:
            raise ValueError("UF deve ter 2 letras (ex: AM)")
        return v


class AnimalPhotoRead(BaseModel):
    id: int
    url: str
    position: int
    class Config:
        from_atributes = True

class AnimalRead(AnimalBase):
    id: int
    owner_id: Optional[int] = None
    likes_count: int = 0
    superlikes_count: int = 0
    image_url: Optional[str] = None  
    photos: list[AnimalPhotoRead] = []
    class Config:
        from_atributes = True



# =========================
# Adoption Requests
# =========================
class AdoptionRequestCreate(BaseModel):
    animal_id: int
    message: Optional[str] = None


class AdoptionRequestStatusUpdate(BaseModel):
    status: AdoptionStatus


class AdoptionRequestRead(BaseModel):
    id: int
    animal_id: int
    user_id: int
    status: AdoptionStatus
    message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ReactionKind(str, Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    SUPERLIKE = "SUPERLIKE"

class ReactionCreate(BaseModel):
    animal_id: int
    kind: ReactionKind

class ReactionRead(BaseModel):
    id: int
    animal_id: int
    user_id: int
    kind: ReactionKind
    model_config = ConfigDict(from_attributes=True)