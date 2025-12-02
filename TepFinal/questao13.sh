#!/bin/bash


generate_numbers() {
    numbers=()
    while [ ${#numbers[@]} -lt 5 ]; do
        num=$((RANDOM % 50 + 1))
        if [[ ! " ${numbers[@]} " =~ " ${num} " ]]; then
            numbers+=($num)
        fi
    done
    echo "${numbers[@]}"
}


save_to_file() {
    data=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$data - ${numbers[@]}" >> lottery_numbers.txt
}


echo "Escolha uma opção:"
echo "1. Exibir números no stdout"
echo "2. Salvar números em arquivo"
read -p "Digite sua escolha: " choice


numbers=$(generate_numbers)

data=$(date "+%Y-%m-%d %H:%M:%S")

if [ "$choice" -eq 1 ]; then
    echo "Data e hora da geração: $data"
    echo "Os números gerados são: ${numbers[@]}"
elif [ "$choice" -eq 2 ]; then
    save_to_file
    echo "Data e hora da geração: $data"
    echo "Os números foram salvos no arquivo."
else
    echo "Escolha inválida!"
fi
