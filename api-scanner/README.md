# 🔍 API Security Scanner

Scanner automatizado de segurança para APIs REST, desenvolvido em Python, com foco em **boas práticas de segurança, detecção de vulnerabilidades comuns e testes automatizados**.

Este projeto foi desenvolvido de forma modular, com suporte a:

- ✅ Logs estruturados
- ✅ Execução em paralelo (multithreading)
- ✅ Testes de headers de segurança
- ✅ Testes de métodos HTTP
- ✅ Testes de CORS
- ✅ Testes de Rate Limit
- ✅ Detecção de XSS refletido
- ✅ Detecção de SQL Injection (heurística)
- ✅ Detecção de Open Redirect

---

## 🚀 Funcionalidades

### 🔐 1. Headers de Segurança
Verifica a presença dos principais headers:
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

---

### 🌐 2. Métodos HTTP (Paralelo)
Testa em paralelo os métodos:
- GET
- POST
- PUT
- DELETE
- OPTIONS

Retorna o status de cada método.

---

### 🌍 3. CORS
Verifica os headers:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Credentials`

---

### 🚦 4. Rate Limit
Dispara várias requisições e tenta detectar:
- Respostas 429 (Too Many Requests)
- Limitação por IP

---

### 🧨 5. XSS (Cross-Site Scripting)
Testa XSS refletido com payloads como:
- `<script>alert(1)</script>`
- `"><img src=x onerror=alert(1)>`

✔ Detecção baseada em reflexão direta do payload no corpo da resposta.

---

### 💉 6. SQL Injection (SQLi)
Testa SQL Injection com payloads como:
- `' OR '1'='1`
- `" OR "1"="1`
- `1 OR 1=1`

✔ Heurística baseada em:
- Status >= 500
- Presença de palavras-chave de erro SQL

---

### 🔓 7. Open Redirect
Testa parâmetros como:
- `next`
- `redirect`
- `url`
- `dest`
- `returnTo`

✔ Detecta redirecionamentos externos via header `Location`.

---
## 🗂 Estrutura do Projeto
api-scanner/
│
├── main.py
├── requirements.txt
├── README.md
│
├── scanner/
│ ├── headers.py
│ ├── methods.py
│ ├── cors.py
│ ├── ratelimit.py
│ ├── xss.py
│ ├── sqli.py
│ ├── redirect.py
│ ├── endpoint_scanner.py
│ └── report.py
│
├── utils/
│ └── logging_config.py
│
├── logs/
│ ├── output.log
│ └── errors.log
│
└── wordLists/
  └──small.txt


---

## 🛠 Requisitos

- Python 3.8+
- Bibliotecas:
  - `requests`

Instalação:

```bash
pip install -r requirements.txt
```
Como executar:
```bash
python3 main.py --url https://httpbin.org/get
python3 main.py --url https://httpbin.org/redirect-to
```
