# 🐶 AdoCÃO API — Sistema de Adoção de Animais

A **AdoCÃO API** é uma aplicação backend desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**, voltada para o gerenciamento de adoção de animais.  
Ela permite o cadastro de usuários, animais disponíveis para adoção e o controle completo de solicitações de adoção.

Este projeto corresponde à implementação das **Partes A e C** do módulo de Banco de Dados, com início da **Parte B (consultas e relatórios)**.

---

## 🚀 Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Uvicorn
- Autenticação com JWT

---

## 📂 Estrutura do Projeto

adocao/
├── app/
│ ├── core/
│ │ ├── config.py
│ │ └── security.py
│ ├── routers/
│ │ ├── auth.py
│ │ ├── animals.py
│ │ └── adoptions.py
│ ├── db.py
│ ├── deps.py
│ ├── models.py
│ ├── schemas.py
│ └── main.py
├── adocao.db
├── requirements.txt
└── README.md

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/luisRibeiro23/Projetos-Proprios-Luis_Henrique_Ribeiro.git
cd Projetos-Proprios-Luis_Henrique_Ribeiro

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
