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
    - se a resposta vem com status 3xx e Location apontando para o payload
    - ou se o Location contém o domínio do payload.
    """
    try:
        logger.info(f"[Redirect] Testando {base_url} com {param_name}={payload_url}")

        # Não seguir automaticamente o redirect pra inspecionar o Location
        resp = requests.get(
            base_url,
            params={param_name: payload_url},
            timeout=5,
            allow_redirects=False,
        )

        status = resp.status_code
        location = resp.headers.get("Location")

        vulnerable = False
        reason = None

        if location:
            # Verifica se o payload está contido no Location
            if payload_url in location:
                vulnerable = True
                reason = f"Location aponta para payload ({location})"
            else:
                # Heurística extra: compara domínio
                loc_host = urlparse(location).netloc
                payload_host = urlparse(payload_url).netloc
                if payload_host and loc_host == payload_host:
                    vulnerable = True
                    reason = f"Location redireciona para domínio externo ({loc_host})"

        if vulnerable and 300 <= status < 400:
            logger.warning(
                f"[Redirect] POSSÍVEL Open Redirect em {base_url} "
                f"param={param_name} -> {location} (status={status})"
            )
        else:
            logger.info(
                f"[Redirect] Nenhum Open Redirect claro em {base_url} "
                f"param={param_name}, status={status}, Location={location}"
            )

        return {
            "param": param_name,
            "payload": payload_url,
            "status_code": status,
            "location": location,
            "vulnerable": bool(vulnerable and 300 <= status < 400),
            "reason": reason,
        }

    except requests.RequestException as e:
        logger.error(f"[Redirect] Erro ao testar Open Redirect em {base_url}: {e}")
        return {
            "param": param_name,
            "payload": payload_url,
            "status_code": None,
            "location": None,
            "vulnerable": False,
            "error": str(e),
        }

def test_open_redirect(
    url: str,
    param_names=None,
    payloads=None,
    max_workers: int = 5,
) -> dict:
    """
    Testa possíveis Open Redirects variando parâmetros e payloads de URL.
    - url: endpoint a ser testado (ex: https://site.com/login)
    - param_names: lista de nomes de parâmetros (se None, usa DEFAULT_REDIRECT_PARAMS)
    - payloads: lista de URLs de teste (se None, usa DEFAULT_REDIRECT_PAYLOADS)
    """
    if param_names is None:
        param_names = DEFAULT_REDIRECT_PARAMS
    if payloads is None:
        payloads = DEFAULT_REDIRECT_PAYLOADS

    logger.info(
        f"🔁 Iniciando testes de Open Redirect em {url} "
        f"com {len(param_names)} parâmetros e {len(payloads)} payloads"
    )

    results = []
    vulnerable = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_case = {}

        for pname in param_names:
            for payload in payloads:
                future = executor.submit(_test_single_open_redirect, url, pname, payload)
                future_to_case[future] = (pname, payload)

        for future in as_completed(future_to_case):
            res = future.result()
            results.append(res)
            if res.get("vulnerable"):
                vulnerable = True

    summary = {
        "url": url,
        "vulnerable": vulnerable,
        "results": results,
    }

    if vulnerable:
        logger.warning(f"🔓 Resultado final Open Redirect: POSSÍVEL vulnerabilidade em {url}")
    else:
        logger.info(f"✅ Resultado final Open Redirect: nenhum Open Redirect óbvio em {url}")

    return summary
