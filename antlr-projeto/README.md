# Compilador / Analisador MiniC com ANTLR4

Este projeto implementa a **frente de compilação** de uma linguagem de programação do tipo C reduzida (MiniC), utilizando o **ANTLR4** para geração do analisador léxico e sintático, e o padrão **Visitor** para percorrer a árvore sintática e executar as ações de análise.

O projeto foi desenvolvido na disciplina de **Compiladores** (UFAM) e faz parte do meu portfólio de projetos acadêmicos.

---

## 🎯 Objetivos do Projeto

- Definir uma gramática formal para a linguagem MiniC.
- Utilizar o ANTLR4 para gerar:
  - Lexer (analisador léxico)
  - Parser (analisador sintático)
- Implementar um `Visitor` para:
  - percorrer a AST (árvore sintática abstrata);
  - realizar verificações semânticas básicas (tipos, identificadores, etc.);
  - **(opcional)** gerar código intermediário em **três endereços (TAC)**.

---

## 🧱 Linguagem MiniC (resumo)

A linguagem utilizada neste projeto é uma versão reduzida do C, contendo, por exemplo:

- **Tipos básicos**: `int`, `float`, `char` (ajuste conforme sua implementação)
- **Declarações de variáveis**
- **Comandos**:
  - Atribuição (`a = b + c;`)
  - Condicionais (`if`, `else`)
  - Laços (`while`, (`for` se implementado))
  - Comandos de bloco `{ ... }`
- **Expressões**:
  - aritméticas (`+`, `-`, `*`, `/`)
  - relacionais (`<`, `>`, `<=`, `>=`, `==`, `!=`)
  - lógicas (`&&`, `||`, `!`)

A especificação exata da linguagem está codificada na gramática `.g4`.

---

## 📂 Estrutura do Projeto

Adapte os nomes conforme sua pasta real, mas algo assim:

```text
antlr-projeto/
├── grammar/
│   └── MiniC.g4             # Gramática ANTLR da linguagem
├── src/
│   ├── Main.java            # Ponto de entrada: recebe arquivo e roda parser/visitor
│   ├── MiniCVisitorImpl.java# Implementação do Visitor
│   ├── SymbolTable.java     # (Opcional) Tabela de símbolos
│   ├── ErrorListener.java   # (Opcional) Tratamento customizado de erros
│   └── ...                  # Demais classes de suporte
├── examples/
│   ├── exemplo1.c           # Exemplos de entrada na linguagem MiniC
│   ├── exemplo2.c
│   └── ...
├── output/
│   ├── exemplo1.tac         # (Opcional) Código de três endereços gerado
│   └── ...
└── README.md
