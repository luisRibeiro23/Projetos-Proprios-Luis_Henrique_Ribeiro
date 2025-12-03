# scanner/methods.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import setup_logger

logger = setup_logger()

def _test_single_method(url, method):
    try:
        if method == "GET":
            resp = requests.get(url, timeout=5)
        elif method == "POST":
            resp = requests.post(url, timeout=5)
        elif method == "PUT":
            resp = requests.put(url, timeout=5)
        elif method == "DELETE":
            resp = requests.delete(url, timeout=5)
        elif method == "OPTIONS":
            resp = requests.options(url, timeout=5)
        else:
            return method, "unsupported"

        logger.info(f"Método {method}: status {resp.status_code}")
        return method, resp.status_code

    except requests.RequestException as e:
        logger.error(f"Erro ao testar método {method} em {url}: {e}")
        return method, "error"

def test_http_methods_parallel(url, methods, max_workers=5):
    results = {}
    logger.info(f"🔁 Iniciando teste de métodos em paralelo para {url}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_method = {
            executor.submit(_test_single_method, url, m): m for m in methods
        }

        for future in as_completed(future_to_method):
            method = future_to_method[future]
            try:
                m, status = future.result()
                results[m] = status
            except Exception as e:
                logger.exception(f"Falha inesperada ao testar método {method}: {e}")
                results[method] = "error"

    logger.info(f"✅ Teste de métodos paralelo concluído: {results}")
    return results
