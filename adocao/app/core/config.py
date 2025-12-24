# app/core/config.py

class Settings:
    def __init__(self) -> None:
        self.PROJECT_NAME = "AdoCÃO API"

        self.SQLALCHEMY_DATABASE_URL = "sqlite:///./adocao.db"

        self.SECRET_KEY = "super-secret-key-mude-isso-depois"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60


settings = Settings()
