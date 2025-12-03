# scanner/cors.py
import requests
from utils.logging_config import setup_logger

logger = setup_logger()

def test_cors(url: str) -> dict:
    """
    Faz uma requisição com header Origin e verifica os headers CORS de resposta.
    """
    logger.info(f"🌐 Testando CORS em {url}")

    try:
        resp = requests.get(
            url,
            headers={"Origin": "https://example.com"},
            timeout=5
        )
    except requests.RequestException as e:
        logger.error(f"Erro ao testar CORS em {url}: {e}")
        return {"error": str(e)}

    allow_origin = resp.headers.get("Access-Control-Allow-Origin")
    allow_credentials = resp.headers.get("Access-Control-Allow-Credentials")

    result = {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Credentials": allow_credentials,
    }

    logger.info(f"Resultado CORS: {result}")
    return result
