import argparse
from scanner.headers import scan_headers
from scanner.methods import scan_methods
from scanner.discovery import discover_endpoints
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(description="API Security Scanner – v1.0")
    parser.add_argument("--url", required=True, help="URL base da API")
    args = parser.parse_args()

    console.print("[bold magenta]Iniciando análise...[/]")

    scan_headers(args.url)
    scan_methods(args.url)
    discover_endpoints(args.url)

    console.print("\n[bold green]Finalizado![/]")

if __name__ == "__main__":
    main()
