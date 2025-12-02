# Segurança da Informação – Atividades Práticas e Análises

Este diretório reúne atividades práticas realizadas na disciplina de **Segurança da Informação** (UFAM) e estudos complementares executados em ambiente Linux.

O foco das atividades inclui:

- Administração e auditoria em sistemas Linux  
- Permissões, usuários e políticas de acesso  
- Automação com Shell Script  
- Inspeção e manipulação de logs  
- Verificações básicas de rede e processos  
- Identificação de vulnerabilidades em sistemas reais  
- Desenvolvimento do **Trabalho Final**, que consistiu em testar a segurança de um site real e documentar vulnerabilidades encontradas

Este diretório é composto apenas por **código e análises práticas**, sem relatórios formais gerados via PDF, reforçando seu caráter aplicado.

---

## 📂 Estrutura Geral

A organização dos diretórios segue esta lógica:


---

## 🧰 Tecnologias e Ferramentas Principais

- **Linux (Ubuntu)**  
- **Shell Script (bash)**  
- Comandos e ferramentas:
  `grep`, `awk`, `sed`, `cut`, `sort`,  
  `chmod`, `chown`,  
  `ps`, `top`, `kill`,  
  `ss` / `netstat`,  
  `find`, `du`, `df`,  
  `journalctl`, etc.

---

## 🛡️ Conteúdo Resumido dos Diretórios

### ✔ `usuarios/`  
Atividades envolvendo:
- criação e exclusão de usuários e grupos,
- gerenciamento de senhas,
- organização de diretórios home,
- permissões básicas e boas práticas.

---

### ✔ `permissoes/`  
Conjunto de exercícios mostrando:
- permissões de leitura, escrita e execução,
- uso de `chmod`, `umask`, `chown`, `chgrp`,
- testes de acesso cruzado,
- simulação de cenários de falha por permissões inadequadas.

---

### ✔ `scripts/`  
Scripts de uso geral, com propósitos como:
- auditoria do sistema,
- coleta de informações de processos,
- diagnóstico rápido de configuração,
- leitura e filtragem automática de arquivos,
- automação de rotinas administrativas.

---

### ✔ `logs/`  
Atividades envolvendo:
- filtragem e seleção de logs com ferramentas de linha de comando,
- identificação de eventos relevantes,
- preparação de dados para auditoria,
- simulação de investigação inicial de incidentes.

---

### ✔ `rede/`  
Atividades focadas em:
- verificar portas abertas,
- testar conectividade,
- examinar processos ligados à rede,
- simular pequenos diagnósticos.

---

### ⭐ **`trabalhofinal/` – Análise de Vulnerabilidades em Site Real**

O Trabalho Final consistiu em:

- Escolher um site real (não crítico nem governamental) para testes *não destrutivos*  
- Realizar **testes de segurança de baixo impacto**, observando:
  - falhas de configuração  
  - diretórios expostos  
  - headers HTTP incompletos  
  - informações sensíveis em respostas  
  - acessos sem autenticação  
  - erros que revelam estrutura interna  
- Documentar as vulnerabilidades encontradas  
- Indicar como elas se relacionam com o **OWASP Top 10**  
- Propor mitigações básicas  
- Demonstrar compreensão prática de análise de superfície de ataque  

> Nenhum ataque invasivo foi realizado — apenas inspeção, coleta de informações e exploração passiva, conforme boas práticas de ética em segurança.

---

## 🎯 Habilidades Demonstradas

- Administração de sistemas Linux  
- Automação com Shell Script  
- Auditoria básica de segurança  
- Manipulação avançada de logs  
- Diagnóstico de configurações vulneráveis  
- Entendimento prático de riscos e mitigação  
- Capacidade de investigar e organizar resultados técnicos  

---
