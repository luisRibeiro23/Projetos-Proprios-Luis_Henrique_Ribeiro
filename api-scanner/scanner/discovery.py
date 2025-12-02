import requests
from rich.console import Console

console = Console()

def discover_endpoints(url_base):
    console.print("\n[bold cyan]=== Descoberta de Endpoints ===[/]")

    try:
        with open("wordLists/small.txt", "r") as f:
            words = [w.strip() for w in f.readlines()]
    except Exception:
        console.print("[red]Wordlist não encontrada[/]")
        return

    if not url_base.endswith("/"):
        url_base += "/"

    for word in words:
        test_url = url_base + word
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code < 400:
                console.print(f"[green]✔ {test_url} → {r.status_code}[/]")
        except:
            pass

