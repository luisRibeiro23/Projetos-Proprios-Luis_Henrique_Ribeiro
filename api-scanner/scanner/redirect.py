# scanner/redirect.py
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import setup_logger

logger = setup_logger()

# Parâmetros típicos usados pra redirect
DEFAULT_REDIRECT_PARAMS = [
    "next",
    "redirect",
    "redirect_url",
    "url",
    "dest",
    "destination",
    "continue",
    "returnTo",
]

# URLs maliciosas de teste (pode trocar por domínio de teste seu)
DEFAULT_REDIRECT_PAYLOADS = [
    "https://evil.com",
    "https://attacker.example",
    "//evil.com",
]

def _test_single_open_redirect(base_url: str, param_name: str, payload_url: str) -> dict:
    """
    Envia um payload de URL em um parâmetro de redirect e verifica:
    - se a r
