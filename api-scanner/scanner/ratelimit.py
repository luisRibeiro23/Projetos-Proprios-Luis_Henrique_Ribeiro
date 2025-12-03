# scanner/ratelimit.py
import time
import requests
from utils.logging_config import setup_logger

logger = setup_logger()

def test_rate_limit(url: str, max_requests: int = 20, delay: float = 0.0) -> dict:
    """
    Dispara várias requisições para tentar identificar se a API responde com 429 (Too Many Requests).
    Retorna contagem de sucessos e 429.
    """
    logger.info(f"🚦 Testando rate limit em {url} com até {max_requests} requisições")

    success = 0
    too_many = 0
    others = {}

    for i in range(1, max_requests + 1):
        try:
            resp = requests.get(url, timeout=5)
            status = resp.status_code

            if status == 429:
                too_many += 1
                logger.warning(f"[{i}] Resposta 429 Too Many Requests")
            elif 200 <= status < 300:
                success += 1
                logger.info(f"[{i}] Sucesso: {status}")
            else:
                others[status] = others.get(status, 0) + 1
                logger.info(f"[{i}] Status inesperado: {status}")

        except requests.RequestException as e:
            logger.error(f"[{i}] Erro na requisição de rate limit: {e}")

        if delay > 0:
            time.sleep(delay)

    result = {
        "success": success,
        "status_429": too_many,
        "others": others,
    }

    logger.info(f"Resultado final rate limit: {result}")
    return result
