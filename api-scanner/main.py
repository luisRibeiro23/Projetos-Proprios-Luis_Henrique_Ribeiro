# main.py
import argparse
from utils.logging_config import setup_logger

# Importa as funções dos módulos do scanner
from scanner.xss import test_xss
from scanner.sqli import test_sqli
from scanner.redirect import test_open_redirect
from scanner.methods import test_http_methods_parallel
from scanner.headers import test_security_headers
from scanner.cors import test_cors
from scanner.ratelimit import test_rate_limit  # repara: arquivo é ratelimit.py

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="API Security Scanner")
    parser.add_argument(
        "--url",
        required=True,
        help="URL base da API para análise"
    )
    args = parser.parse_args()
    url = args.url

    logger.info("🚀 Iniciando análise da API")
    logger.info(f"Alvo: {url}")

    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    try:
        # 1) Headers de segurança
        headers_result = test_security_headers(url)
        logger.info(f"Resultado headers: {headers_result}")

        # 2) Métodos HTTP (em paralelo)
        methods_result = test_http_methods_parallel(url, methods)
        logger.info("📊 Resultado dos testes de métodos HTTP:")
        for m, status in methods_result.items():
            logger.info(f" - {m}: {status}")

        # 3) CORS
        cors_result = test_cors(url)
        logger.info(f"Resultado CORS: {cors_result}")

        # 3.5) XSS (teste básico em parâmetro de query)
        xss_result = test_xss(url, param_name="q")
        logger.info(f"Resultado XSS: vulnerável={xss_result['vulnerable']}")
         # 3.6) SQL Injection
        sqli_result = test_sqli(url, param_name="id")
        logger.info(f"Resultado SQLi: vulnerável={sqli_result['vulnerable']}")
        # 3.7) Open Redirect
        redirect_result = test_open_redirect(url)
        logger.info(f"Resultado Open Redirect: vulnerável={redirect_result['vulnerable']}")
        # 4) Rate limit
        rate_limit_result = test_rate_limit(url)
        logger.info(f"Resultado rate limit: {rate_limit_result}")

        logger.info("✅ Análise concluída com sucesso.")

    except Exception as e:
        logger.exception(f"❌ Erro inesperado durante a análise: {e}")

if __name__ == "__main__":
    main()
