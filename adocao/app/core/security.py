from datetime import datetime, timedelta
from typing import Optional
from jose import jwt 
from passlib.context import CryptContext

# Usando PBKDF2-SHA256 para simplificar (sem dor de cabeça com bcrypt)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


SECRET_KEY = "changeme-super-secret-key"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 60


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_acess_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt