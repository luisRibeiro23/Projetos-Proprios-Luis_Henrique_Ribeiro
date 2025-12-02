import requests
from rich.console import Console

console = Console()

TEST_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

def scan_methods(url):
    console.print("\n[bold cyan]=== Teste de Métodos HTTP ===[/]")

    for method in TEST_METHODS:
        try:
            r = requests.request(method, url, timeout=5)
            console.print(f"[white]{method}[/]: [green]{r.status_code}[/]")
        except Exception:
            console.print(f"[white]{method}[/]: [red]Falhou[/]")

