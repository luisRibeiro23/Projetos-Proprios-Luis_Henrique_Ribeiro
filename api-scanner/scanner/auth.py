import requests 
import jwt
from rich.console import Console

console = Console()

def test_auth(url, token):
  console.print("\n[bold cyan]=== Teste de autenticação (JWT) ===[/]")
  
  #1 teste sem token
  r_no_token = requests.get(url)
  console.print(f"[yellow]Sem token → {r_no_token.status_code}[/]")
  
  #2 Teste com token inválido
  headers_invalid = {"Authorization": "Bearer INVALID123"
  r_invalid = requests.get(url, headers=head_invalid)
  console.print(f"[red]Token inválido → {r_invalid.status_code}[/]")
  
  #3 Teste com token adulterado (se JWT for inválido)
  try:
    parts = token.split(".")
    parts[1] = "AAAAAAAAAA"
    tampered_token = ".".join(parts)
    headers_tampered = {"Authorization": f"Beares {tampered_token}"}
    r_tampered = requests.get(url, headers=headers_tampered)
    console.print(f"[red]Token adulterado → {r_tampered.status_code}[/]")
  except:
    console.print("[blue]Token não parece ser JWT, pulando adulteração[/]")
    
