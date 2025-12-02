# PIXI API – Exploração de Vulnerabilidades (API Security)

Este diretório contém todas as quatro partes da atividade prática envolvendo a **PIXI API**, um ambiente vulnerável projetado para ensino de segurança em APIs.

As atividades exploram várias vulnerabilidades relacionadas ao **OWASP API Security Top 10**, além de testar endpoints via Postman e manipular JWTs.

---

# 📘 Parte 1 – Especificação da API  
:contentReference[oaicite:2]{index=2}

- Instalação do PIXI.
- Geração da documentação **OpenAPI 3.0.X**.
- Análise estrutural dos endpoints disponibilizados.

**Entregável**: arquivo JSON contendo o OAS completo da API.

---

# 🔐 Parte 2 – Exploração das Vulnerabilidades API1, API3 e API7  
:contentReference[oaicite:3]{index=3}

### 🔸 **API1 – Broken Object Level Authorization (BOLA)**  
Exploração baseada na manipulação de **JWT**, permitindo acesso a dados de usuários diferentes.

### 🔸 **API7 – Security Misconfiguration**  
Descoberta da *secret key* usada para assinar os tokens JWT.

### 🔸 **API3 – Excessive Data Exposure**  
A partir da adulteração do token, foi possível extrair informações completas de **todos os usuários cadastrados** via `GET /user_info`.

**Entregáveis**:
- JWTs modificados
- Lista de dados extraídos
- Prints das requisições e respostas

---

# 🔒 Parte 3 – Exploração das vulnerabilidades API5, API6 e API9  
:contentReference[oaicite:4]{index=4}

### 🔸 **API6 – Mass Assignment**  
Elevação de privilégios alterando atributos de conta (tornando um usuário comum em administrador).

### 🔸 **API5 – Broken Function Level Authorization**  
Após elevar privilégios, foi possível acessar **endpoints exclusivos de administradores**.

### 🔸 **API9 – Improper Assets Management**  
Descoberta de endpoints não documentados e inconsistências entre código e OAS.

**Entregável**:  
Coleção de prints mostrando execução de endpoints administrativos usando JWT adulterado.

---

# 📮 Parte 4 – Teste de Métodos da API via Postman  
:contentReference[oaicite:5]{index=5}

Criação de uma coleção consolidada contendo:

- Todos os métodos do PIXI
- Requisições e respostas completas
- Testes de erro e sucesso
- Endpoints funcionais + endpoints problemáticos

---

# 📁 Estrutura da Pasta

---

# 🧠 Habilidades Demonstradas

- Manipulação e adulteração de JWT  
- Entendimento profundo do **OWASP API Security Top 10**  
- Teste de APIs vulneráveis  
- Análise de inconsistências entre documentação OAS e código  
- Elevação de privilégios por Mass Assignment  
- Teste de endpoints administrativos  
- Uso avançado do Postman  
- Escrita técnica de vulnerabilidades  

---

# 🏁 Status
Todas as quatro partes do projeto foram concluídas com sucesso.
