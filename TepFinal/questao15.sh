#!/bin/bash

# Função para converter caractere para número
atoi() {
    echo "$1" | od -An -t dC | awk '{print $1}'
}

# Teste da função
read -p "Digite um caractere para converter para número: " char
atoi "$char"
