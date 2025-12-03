# scanner/xss.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import setup_logger

logger = setup_logger()

# Alguns payloads básicos de XSS (pode expandir depois ou ler de wordLists)
DEFAULT_XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
]

def _test_single_xss(url: str, param_name: str, payload: str) -> dict:
    """
    Envia um payload XSS em um parâmetro e verifica se ele volta refletido na resposta.
    Heurística simples: se o payload aparece "cru" no corpo, marcamos como possível XSS.
    """
    try:
        logger.info(f"[XSS] Testando payload em {url} param={param_name}")
        resp = requests.get(url, params={param_name: payload}, timeout=5)

        body = resp.text

        reflected = payload in body

        result = {
            "payload": payload,
            "status_code": resp.status_code,
            "reflected": reflected,
        }

        if reflected:
            logger.warning(f"[XSS] Payload refletido! POSSÍVEL XSS em {url} ({param_name})")
        else:
            logger.info(f"[XSS] Payload não refletido em {url} ({param_name})")

        return result

    except requests.RequestException as e:
        logger.error(f"[XSS] Erro ao testar payload em {url}: {e}")
        return {
            "payload": payload,
            "error": str(e),
            "reflected": False,
        }

def test_xss(
    url: str,
    param_name: str = "q",
    payloads=None,
    max_workers: int = 5
) -> dict:
    """
    Testa XSS refletido enviando vários payloads em um parâmetro de query.
    - url: endpoint a ser testado (ex: https://example.com/search)
    - param_name: nome do parâmetro de query (ex: "q", "search", etc.)
    - payloads: lista opcional de payloads XSS. Se None, usa DEFAULT_XSS_PAYLOADS.

    Retorna um dict com:
    {
        "url": ...,
        "param": ...,
        "vulnerable": True/False,
        "results": [ {payload, status_code, reflected, error?}, ... ]
    }
    """
    if payloads is None:
        payloads = DEFAULT_XSS_PAYLOADS

    logger.info(f"🧨 Iniciando testes de XSS em {url} param={param_name} com {len(payloads)} payloads")

    results = []
    vulnerable = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_payload = {
            executor.submit(_test_single_xss, url, param_name, p): p for p in payloads
        }

        for future in as_completed(future_to_payload):
            res = future.result()
            results.append(res)
            if res.get("reflected"):
                vulnerable = True

    summary = {
        "url": url,
        "param": param_name,
        "vulnerable": vulnerable,
        "results": results,
    }

    if vulnerable:
        logger.warning(f"🧨 Resultado final XSS: POSSÍVEL vulnerabilidade detectada em {url}")
    else:
        logger.info(f"✅ Resultado final XSS: nenhum payload refletido em {url}")

    return summary
