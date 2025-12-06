# app/core/config.py

class Settings:
    # Caminho do banco. Pode mudar o nome do arquivo se quiser.
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./adocao.db"

settings = Settings()
