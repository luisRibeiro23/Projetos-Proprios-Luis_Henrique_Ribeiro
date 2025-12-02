# 🐍 Jogo da Cobrinha (Snake) – Versão Automatizada / Bot

Este projeto implementa o clássico **jogo da cobrinha (Snake)**, porém com um diferencial:  
a cobra **não é controlada pelo jogador**, mas sim por um **algoritmo automatizado** capaz de jogar sozinha.

O projeto foi desenvolvido como parte do meu portfólio pessoal e demonstra habilidades em lógica, estruturas de dados, programação de jogos e estratégias para automação.

---

## 🎯 Objetivos do Projeto

- Recriar o jogo Snake com movimentação, comida, colisões e placar.  
- Desenvolver um **bot** capaz de tomar decisões em tempo real.  
- Demonstrar:
  - lógica de jogos baseada em grade (grid),
  - detecção de colisão,
  - atualizações do estado do jogo (game loop),
  - estratégia automatizada para navegar no mapa.

---

## 🤖 Como o Bot Funciona

A lógica do bot pode variar conforme sua implementação real, mas o conceito geral é:

- A cada frame, o bot analisa a posição atual da cobra e da comida.  
- Tenta seguir o caminho mais seguro até o alimento.  
- Evita paredes e colisões com o próprio corpo.  
- Caso o caminho direto seja arriscado, escolhe rota alternativa.  

Exemplos de estratégias que podem ser usadas (ajuste conforme seu código):

- Movimento guloso (sempre tentar se aproximar da comida).  
- Controle de risco: desviar do próprio corpo.  
- Movimentação de escape quando preso em “becos”.  
- Estratégia baseada em prioridades (ex: comida → segurança → giro).  

Se quiser, posso escrever uma seção descrevendo a lógica EXATA do seu bot ao ver o código.

---

## 🛠 Tecnologias Utilizadas

- Linguagem: ***Java***    
- Paradigma: programação estruturada / orientada a objetos  
- Controle de estado via game loop

---

## 📂 Estrutura do Projeto




