# utils/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger():
    """Configura dois loggers: um geral e um de erros."""
    logger = logging.getLogger("api_scanner")
    logger.setLevel(logging.DEBUG)

    # Evita adicionar handlers duplicados se já foi configurado
    if logger.handlers:
        return logger

    # Formatter padrão
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Log geral
    info_handler = RotatingFileHandler(
        LOG_DIR / "output.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Log de erros
    error_handler = RotatingFileHandler(
        LOG_DIR / "errors.log",
        maxBytes=500_000,
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Log no console também (pra ver na hora)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger
