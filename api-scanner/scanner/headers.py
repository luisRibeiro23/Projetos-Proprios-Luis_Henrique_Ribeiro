import requests
from rich.console import Console

console = Console()

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

def scan_headers(url):
    console.print("\n[bold cyan]=== Teste de Headers de Segurança ===[/]")

    try:
        r = requests.get(url, timeout=5)
    except Exception as e:
        console.print(f"[red]Erro ao acessar {url}: {e}[/]")
        return

    for header in SECURITY_HEADERS:
        if header in r.headers:
            console.print(f"[green]✔ {header} presente[/]")
        else:
            console.print(f"[red]✘ {header} ausente[/]")

    console.print("[yellow]Headers coletados:[/]")
    for k, v in r.headers.items():
        console.print(f" [white]{k}[/]: {v}")

