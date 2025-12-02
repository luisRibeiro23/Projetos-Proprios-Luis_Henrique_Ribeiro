import requests 
from rich.console import Console 
import time

console = Console()

def test_rate_limit(url):
  console.print("\n[bold cyan]=== Teste de Rate Limit ===[/]")

  success = 0
  too_many = 0

  for i in range(15):
    r = requests.get(url)
    if r.status_code == 429:
      too_many += 1
    else:
      success += 1
    time.sleep(0.2)
  console.print(f"[green]Sucesso: {success}[/]")
  console.print(f"[red]429 Too Many Requests: {too_many}[/]")
  
