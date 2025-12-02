from scanner.headers import scan_headers
from scanner.methods import scan_methods
from scanner.discovery import discover_endpoints
from scanner.auth import test_auth

import argparse

def main():
    parser = argparse.ArgumentParser(description="API Security Scanner v1.0")
    parser.add_argument("--url", required=True, help="Base URL da API")
    parser.add_argument("--token", help="Token JWT opcional")
    args = parser.parse_args()

    print("[*] Iniciando análise da API:", args.url)

    scan_headers(args.url)
    scan_methods(args.url)
    discover_endpoints(args.url)
    
    if args.token:
        test_auth(args.url, args.token)

if __name__ == "__main__":
    main()
