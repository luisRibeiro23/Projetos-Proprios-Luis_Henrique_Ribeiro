#!/bin/bash

gerar_chave() {
    local palavra_chave="$1"
    local alfabeto="ABCDEFGHIKLMNOPQRSTUVWXYZ"
    local chave_final=""
    local usado=""

    palavra_chave=$(echo "$palavra_chave" | tr '[:lower:]' '[:upper:]' | tr -d 'J')

    for ((i = 0; i < ${#palavra_chave}; i++)); do
        letra="${palavra_chave:i:1}"
        if [[ "$usado" != *"$letra"* ]]; then
            chave_final+="$letra"
            usado+="$letra"
        fi
    done

    for ((i = 0; i < ${#alfabeto}; i++)); do
        letra="${alfabeto:i:1}"
        if [[ "$usado" != *"$letra"* ]]; then
            chave_final+="$letra"
            usado+="$letra"
        fi
    done

    echo "$chave_final"
}


buscar_posicao() {
    local letra="$1"
    local quadrado="$2"

    for ((i = 0; i < ${#quadrado}; i++)); do
        if [[ "${quadrado:i:1}" == "$letra" ]]; then
            echo "$((i / 5)) $((i % 5))"
            return
        fi
    done
}


criptografar_digrama() {
    local digrama="$1"
    local quadrado="$2"
    local direcao="$3"

    local letra1="${digrama:0:1}"
    local letra2="${digrama:1:1}"
    local pos1=($(buscar_posicao "$letra1" "$quadrado"))
    local pos2=($(buscar_posicao "$letra2" "$quadrado"))

    local linha1="${pos1[0]}" col1="${pos1[1]}"
    local linha2="${pos2[0]}" col2="${pos2[1]}"

    if [[ "$linha1" -eq "$linha2" ]]; then
        col1=$(( (col1 + direcao) % 5 ))
        col2=$(( (col2 + direcao) % 5 ))
    elif [[ "$col1" -eq "$col2" ]]; then
        linha1=$(( (linha1 + direcao) % 5 ))
        linha2=$(( (linha2 + direcao) % 5 ))
    else
        temp="$col1"
        col1="$col2"
        col2="$temp"
    fi

    local nova1="${quadrado:((linha1 * 5 + col1)):1}"
    local nova2="${quadrado:((linha2 * 5 + col2)):1}"

    echo "$nova1$nova2"
}


cifrar_mensagem() {
    local texto="$1"
    local quadrado="$2"
    local direcao="$3"

    texto=$(echo "$texto" | tr '[:lower:]' '[:upper:]' | tr -d ' ' | tr 'J' 'I')
    local digramas=()
    local resultado=""

    while [[ -n "$texto" ]]; do
        local l1="${texto:0:1}"
        local l2="${texto:1:1}"

        if [[ "$l1" == "$l2" || -z "$l2" ]]; then
            digramas+=("${l1}X")
            texto="${texto:1}"
        else
            digramas+=("${l1}${l2}")
            texto="${texto:2}"
        fi
    done

    for digrama in "${digramas[@]}"; do
        resultado+=$(criptografar_digrama "$digrama" "$quadrado" "$direcao")
    done

    echo "$resultado"
}


echo "Bem-vindo à Cifra Playfair!"
read -p "Insira a palavra-chave: " palavra_chave

chave=$(gerar_chave "$palavra_chave")

echo -e "\nChave gerada (5x5):"
for ((i = 0; i < ${#chave}; i += 5)); do
    echo "${chave:i:5}"
done

read -p "Digite a mensagem para criptografar: " mensagem
criptografada=$(cifrar_mensagem "$mensagem" "$chave" 1)
echo -e "\nMensagem criptografada: $criptografada"

descriptografada=$(cifrar_mensagem "$criptografada" "$chave" -1)
echo -e "Mensagem descriptografada: $descriptografada"
