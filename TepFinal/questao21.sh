#!/bin/bash

# Caminho para o dicionário
DICIONARIO="./dicionario.txt"

# Verificar se o dicionário existe
if [[ ! -f $DICIONARIO ]]; then
    echo "Dicionário não encontrado em $DICIONARIO."
    exit 1
fi

# Criar um arquivo temporário para o dicionário
DICIONARIO_TEMP=$(mktemp)
tr '[:upper:]' '[:lower:]' < "$DICIONARIO" > "$DICIONARIO_TEMP"

# Função que verifica se duas palavras diferem por uma única letra
diferem_em_uma_letra() {
    local p1="$1"
    local p2="$2"
    local divergencias=0

    for ((i=0; i<${#p1}; i++)); do
        if [[ "${p1:i:1}" != "${p2:i:1}" ]]; then
            divergencias=$((divergencias + 1))
        fi
    done

    [[ $divergencias -eq 1 ]]
}

# Função que encontra a escada de palavras entre as palavras inicial e final
buscar_escada() {
    local palavra_inicial="$1"
    local palavra_final="$2"
    local fila_palavras=("$palavra_inicial")  # Fila de palavras a serem processadas
    local palavras_visitadas=("$palavra_inicial")  # Lista de palavras já visitadas
    local caminhos_atuais=("$palavra_inicial")  # Caminho até a palavra atual

    # Processo de busca em largura (BFS)
    while [[ ${#fila_palavras[@]} -gt 0 ]]; do
        local palavra_atual="${fila_palavras[0]}"
        local caminho_atual="${caminhos_atuais[0]}"
        fila_palavras=("${fila_palavras[@]:1}")
        caminhos_atuais=("${caminhos_atuais[@]:1}")

        while IFS= read -r palavra; do
            if diferem_em_uma_letra "$palavra_atual" "$palavra"; then
                # Quando encontrar a palavra final
                if [[ "$palavra" == "$palavra_final" ]]; then
                    echo "$caminho_atual -> $palavra"
                    rm "$DICIONARIO_TEMP"
                    exit 0
                fi

                # Se a palavra ainda não foi visitada, adiciona à fila
                if [[ ! " ${palavras_visitadas[@]} " =~ " $palavra " ]]; then
                    fila_palavras+=("$palavra")
                    caminhos_atuais+=("$caminho_atual -> $palavra")
                    palavras_visitadas+=("$palavra")
                fi
            fi
        done < <(grep "^.\{${#palavra_inicial}\}$" "$DICIONARIO_TEMP")  # Garante palavras do mesmo tamanho
    done

    echo "Não foi possível encontrar uma escada entre '$palavra_inicial' e '$palavra_final'."
    rm "$DICIONARIO_TEMP"
}

# Entrada das palavras
read -p "Informe a palavra inicial: " palavra_inicial
read -p "Informe a palavra final: " palavra_final

# Verificar se as palavras possuem o mesmo comprimento
if [[ ${#palavra_inicial} -ne ${#palavra_final} ]]; then
    echo "As palavras devem ter o mesmo número de caracteres."
    exit 1
fi

# Converter as palavras para minúsculas
palavra_inicial=$(echo "$palavra_inicial" | tr '[:upper:]' '[:lower:]')
palavra_final=$(echo "$palavra_final" | tr '[:upper:]' '[:lower:]')

# Buscar a escada entre as palavras
buscar_escada "$palavra_inicial" "$palavra_final"
