# scanner/endpoint_scanner.py
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from utils.logging_config import setup_logger

logger = setup_logger()

def scan_single_endpoint(base_url, path):
    url = base_url.rstrip("/") + path
    try:
        resp = requests.get(url, timeout=5)
        logger.info(f"[{resp.status_code}] {url}")
        return {
            "path": path,
            "url": url,
            "status": resp.status_code,
            "length": len(resp.content)
        }
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar {url}: {e}")
        return {
            "path": path,
            "url": url,
            "status": "error",
            "error": str(e)
        }

def scan_endpoints_parallel(base_url, endpoints, max_workers=10):
    logger.info(f"🧵 Iniciando scan paralelo de {len(endpoints)} endpoints")
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {
            executor.submit(scan_single_endpoint, base_url, path): path
            for path in endpoints
        }

        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                logger.exception(f"Erro inesperado ao processar endpoint {path}: {e}")

    logger.info("✅ Scan paralelo de endpoints concluído")
    return results
