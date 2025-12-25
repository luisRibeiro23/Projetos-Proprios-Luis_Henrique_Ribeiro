# 🐶 AdoCÃO – Sistema de Adoção de Animais

Sistema web completo para adoção de animais, com backend em FastAPI e frontend em React (Vite),
implementando autenticação, autorização por papéis e fluxo completo de adoção.

---

## 🔗 Links
- **Frontend (Netlify):** https://stately-cajeta-17b2b6.netlify.app
- **Backend (Render):** https://adocao-api-lnq1.onrender.com
- **Repositório:** https://github.com/luisRibeiro23/Projetos-Proprios-Luis_Henrique_Ribeiro

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python + FastAPI**
- **JWT (Bearer Token)**
- **SQLAlchemy + SQLite**
- **Pydantic (validação de dados)**
- **CORS configurado**
- **Upload e serviço de arquivos estáticos**
- **Deploy no Render**

### Frontend
- **React + Vite**
- **Fetch API**
- **Controle de autenticação via token**
- **Rotas protegidas**
- **Deploy no Netlify**

---

## 🔐 Segurança Implementada

- Autenticação com **JWT**
- Senhas armazenadas com **hash (bcrypt)**
- **Autorização por papéis**:
  - ONG
  - Adotante
  - Doador
- Validação rigorosa de dados (Pydantic)
- CORS restrito ao domínio do frontend

---

## 🔄 Funcionalidades

- Cadastro e login de usuários
- Diferenciação de usuários por papel
- Cadastro, edição e remoção de animais (ONG)
- Solicitação de adoção (Adotante)
- Controle de status de adoção
- Visualização de perfil do animal
- Upload e exibição de imagens
- Dashboards por tipo de usuário

---

## 📦 Como rodar localmente

### Backend
```bash
cd adocao
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
