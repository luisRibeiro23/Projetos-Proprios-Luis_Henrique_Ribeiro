# scanner/headers.py
import requests
from utils.logging_config import setup_logger

logger = setup_logger()

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

def test_security_headers(url: str) -> dict:
    """
    Faz uma requisição GET e verifica a presença dos principais headers de segurança.
    Retorna um dict: {header: True/False, ...}
    """
    logger.info(f"🛡️ Testando headers de segurança em {url}")

    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Erro ao testar headers em {url}: {e}")
        return {"error": str(e)}

    results = {}
    for h in SECURITY_HEADERS:
        present = h in resp.headers
        results[h] = present
        if present:
            logger.info(f"Header presente: {h}")
        else:
            logger.warning(f"Header AUSENTE: {h}")

    return results
