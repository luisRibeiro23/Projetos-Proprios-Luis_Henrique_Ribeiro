# 🔍 API Security Scanner  
Um scanner leve para análise automática de APIs REST.  
Desenvolvido para fins educacionais, prática de segurança e portfólio.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![Category](https://img.shields.io/badge/category-security-critical)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🧠 Sobre o projeto

O **API Security Scanner** é uma ferramenta CLI que realiza testes automáticos em APIs REST com foco em:

- **Headers de segurança**
- **Métodos HTTP aceitos**
- **Descoberta leve de endpoints**
- **CORS**
- **Rate limit**
- **Autenticação (JWT ou Bearer Tokens)**  
- (Em desenvolvimento) **Relatórios JSON/HTML**, **fuzzing leve**, **validação de payload**, etc.

O objetivo do projeto é oferecer uma ferramenta didática, simples e expandível, ideal para estudantes e entusiastas de segurança explorarem conceitos de pentest em APIs de forma ética.

---

# 🚀 Instalação

Clone o repositório:

```bash
git clone https://github.com/luisRibeiro23/Projetos-Proprios-Luis_Henrique_Ribeiro
cd Projetos-Proprios-Luis_Henrique_Ribeiro/api-scanner
pip install -r requirements.txt
```
# Uso Basico

**python3 main.py --url https://api.com**
**python3 main.py --url https://api.com/users --token SEU_TOKEN_AQUI**

=== Teste de Headers de Segurança ===
✔ Content-Security-Policy presente
✔ Strict-Transport-Security presente
✔ X-Frame-Options presente
✔ X-Content-Type-Options presente
✔ Referrer-Policy presente

=== Teste de Métodos HTTP ===
GET: 200
POST: 404
PUT: 404
DELETE: 404
OPTIONS: 204

=== Descoberta de Endpoints ===
✔ https://api.github.com/users → 200
✔ https://api.github.com/status → 200

=== Teste de CORS ===
CORS vulnerável! Allow-Origin: *

=== Teste de Rate Limit ===
Sucesso: 15
429 Too Many Requests: 0

=== Teste de Headers de Segurança ===
✘ Content-Security-Policy ausente
✘ Strict-Transport-Security ausente
✘ X-Frame-Options ausente
✘ X-Content-Type-Options ausente
✘ Referrer-Policy ausente

=== Teste de Métodos HTTP ===
GET: 200
POST: 404
PUT: 404
DELETE: 404

=== Descoberta de Endpoints ===
✔ https://jsonplaceholder.typicode.com/users → 200
✔ https://jsonplaceholder.typicode.com/ → 200

=== Teste de CORS ===
CORS vulnerável! Allow-Origin: http://malicious-site.com
Allow-Credentials: true

=== Teste de Rate Limit ===
Sucesso: 15
429 Too Many Requests: 0

