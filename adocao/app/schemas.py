from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


# ==== ENUMS ==== #

class UserRole(str, Enum):
    ADOTANTE = "ADOTANTE"
    ONG = "ONG"


class Species(str, Enum):
    CAO = "CAO"
    GATO = "GATO"
    OUTRO = "OUTRO"


class Size(str, Enum):
    PEQUENO = "PEQUENO"
    MEDIO = "MEDIO"
    GRANDE = "GRANDE"


class Sex(str, Enum):
    MACHO = "MACHO"
    FEMEA = "FEMEA"


class AnimalStatus(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_ANALISE = "EM_ANALISE"
    ADOTADO = "ADOTADO"


class AdoptionStatus(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


# ==== USERS ==== #

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.ADOTANTE
    city: Optional[str] = None
    state: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==== ANIMALS ==== #

class AnimalBase(BaseModel):
    name: str
    # se quiser aproveitar os enums, pode trocar para: species: Species
    species: str
    # e aqui: size: Size
    size: str
    age: str
    description: Optional[str] = None
    city: str
    state: str
    available: bool = True


class AnimalCreate(AnimalBase):
    """Campos necessários para criar animal"""
    pass


class Animal(BaseModel):
    # se você estiver usando isso em algum lugar:
    id: int
    # herdar do AnimalBase também é ok, mas não é obrigatório
    name: str
    species: str
    size: str
    age: str
    description: Optional[str] = None
    city: str
    state: str
    available: bool = True

    model_config = ConfigDict(from_attributes=True)


class AnimalRead(AnimalBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==== ADOPTION REQUESTS ==== #

class AdoptionRequestBase(BaseModel):
    message: Optional[str] = None


class AdoptionRequestCreate(AdoptionRequestBase):
    # user_id NÃO vem do body, vamos pegar do usuário logado
    user_id: int
    animal_id: int


class AdoptionRequestUpdateStatus(BaseModel):
    status: AdoptionStatus


class AdoptionRequestRead(AdoptionRequestBase):
    id: int
    animal_id: int
    user_id: int
    status: AdoptionStatus   
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==== LIST WRAPPERS (opcionais) ==== #

class AnimalsList(BaseModel):
    items: List[AnimalRead]


class AdoptionRequestsList(BaseModel):
    items: List[AdoptionRequestRead]


# ==== AUTH ==== #

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
