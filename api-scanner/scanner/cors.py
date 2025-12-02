import requests
from rich.console import Console

console = Console()

def test_cors(url):
    console.print("\n[bold cyan]=== Teste de CORS ===[/]")

    test_origin = "http://malicious-site.com"
    headers = {"Origin": test_origin}

    try:
        r = requests.get(url, headers=headers, timeout=5)
        acao = r.headers.get("Access-Control-Allow-Origin", "Nenhum")

        if acao == "*" or acao == test_origin:
            console.print(f"[red]CORS vulnerável! Allow-Origin: {acao}[/]")
        else:
            console.print(f"[green]CORS seguro. Allow-Origin: {acao}[/]")

        acc = r.headers.get("Access-Control-Allow-Credentials", "Nenhum")
        console.print(f"[yellow]Allow-Credentials: {acc}[/]")

    except Exception as e:
        console.print(f"[red]Erro ao testar CORS: {e}[/]")
