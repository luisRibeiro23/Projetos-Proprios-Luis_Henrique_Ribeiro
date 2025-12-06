# app/models.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from .db import Base
from .schemas import AdoptionStatus 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="ADOTANTE")  # ADOTANTE, ONG, ADMIN
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relacionamento com animais (uma ONG pode cadastrar vários animais, por exemplo)
    animals = relationship("Animal", back_populates="owner")
    adoption_requests = relationship("AdoptionRequest", back_populates="user")


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    size = Column(String, nullable=False)
    age = Column(String, nullable=False)
    description = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="animals")
    adoption_requests = relationship("AdoptionRequest", back_populates="animal")  # ✅ AQUI



 # se não tiver, importa

class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        String(50),
        nullable=False,
        default=AdoptionStatus.PENDENTE.value  # "PENDENTE"
    )
    message = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="adoption_requests")
    animal = relationship("Animal", back_populates="adoption_requests")
