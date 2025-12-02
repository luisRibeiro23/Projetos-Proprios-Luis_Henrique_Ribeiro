from scanner.headers import scan_headers
from scanner.methods import scan_methods
from scanner.discovery import discover_endpoints
from scanner.auth import test_auth
from scanner.cors import test_cors
from scanner.ratelimit import test_rate_limit

from rich.console import Console
import argparse

console = Console()

def main():
    parser = argparse.ArgumentParser(description="API Security Scanner – v2.0")
    parser.add_argument("--url", required=True)
    parser.add_argument("--token", help="Token JWT opcional")
    args = parser.parse_args()

    console.print("[bold magenta]Iniciando análise...[/]")

    scan_headers(args.url)
    scan_methods(args.url)
    discover_endpoints(args.url)
    test_cors(args.url)
    test_rate_limit(args.url)

    if args.token:
        test_auth(args.url, args.token)

    console.print("\n[bold green]Finalizado![/]")

if __name__ == "__main__":
    main()
