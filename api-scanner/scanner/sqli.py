# scanner/sqli.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import setup_logger

logger = setup_logger()

# Payloads básicos de SQLi (pode expandir ou mover para wordLists depois)
DEFAULT_SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1",
    "1 OR 1=1",
    "1' OR '1'='1' --",
    "admin'--",
    "'; DROP TABLE users; --",
]

SQL_ERROR_KEYWORDS = [
    "sql syntax",
    "mysql",
    "postgresql",
    "sqlite",
    "oracle",
    "syntax error",
    "unclosed quotation mark",
    "odbc",
    "sqlstate",
]

def _analyze_sql_error(body_lower: str) -> list:
    """Procura palavras-chave de erro SQL no corpo da resposta (lowercase)."""
    found = []
    for kw in SQL_ERROR_KEYWORDS:
        if kw in body_lower:
            found.append(kw)
    return found

def _test_single_sqli(url: str, param_name: str, payload: str) -> dict:
    """
    Envia um payload de SQLi em um parâmetro e verifica:
    - status code (500/erro pode indicar algo)
    - presença de mensagens de erro SQL no corpo.
    """
    try:
        logger.info(f"[SQLi] Testando payload em {url} param={param_name}")
        resp = requests.get(url, params={param_name: payload}, timeout=5)

        body_lower = resp.text.lower()
        status = resp.status_code
        error_keywords = _analyze_sql_error(body_lower)

        # Heurística simples:
        # - status 500 ou similar
        # - ou erro SQL explícito no corpo
        possible_vuln = bool(error_keywords) or status >= 500

        if possible_vuln:
            logger.warning(
                f"[SQLi] POSSÍVEL vulnerabilidade em {url} ({param_name}) "
                f"status={status}, erros={error_keywords}"
            )
        else:
            logger.info(
                f"[SQLi] Nenhum sinal claro de SQLi em {url} ({param_name}), status={status}"
            )

        return {
            "payload": payload,
            "status_code": status,
            "sql_error_keywords": error_keywords,
            "possible_vulnerable": possible_vuln,
        }

    except requests.RequestException as e:
        logger.error(f"[SQLi] Erro ao testar payload em {url}: {e}")
        return {
            "payload": payload,
            "error": str(e),
            "status_code": None,
            "sql_error_keywords": [],
            "possible_vulnerable": False,
        }

def test_sqli(
    url: str,
    param_name: str = "id",
    payloads=None,
    max_workers: int = 5,
) -> dict:
    """
    Testa SQL Injection enviando vários payloads em um parâmetro de query.
    - url: endpoint a ser testado (ex: https://example.com/users)
    - param_name: nome do parâmetro (ex: "id", "user_id", etc.)
    - payloads: lista de payloads; se None, usa DEFAULT_SQLI_PAYLOADS.

    Retorna:
    {
        "url": ...,
        "param": ...,
        "vulnerable": True/False,
        "results": [ {payload, status_code, sql_error_keywords, possible_vulnerable, error?}, ... ]
    }
    """
    if payloads is None:
        payloads = DEFAULT_SQLI_PAYLOADS

    logger.info(
        f"💉 Iniciando testes de SQLi em {url} param={param_name} com {len(payloads)} payloads"
    )

    results = []
    vulnerable = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_payload = {
            executor.submit(_test_single_sqli, url, param_name, p): p
            for p in payloads
        }

        for future in as_completed(future_to_payload):
            res = future.result()
            results.append(res)
            if res.get("possible_vulnerable"):
                vulnerable = True

    summary = {
        "url": url,
        "param": param_name,
        "vulnerable": vulnerable,
        "results": results,
    }

    if vulnerable:
        logger.warning(f"💉 Resultado final SQLi: POSSÍVEL vulnerabilidade em {url}")
    else:
        logger.info(f"✅ Resultado final SQLi: nenhum sinal claro de SQLi em {url}")

    return summary
