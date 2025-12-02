#!/bin/bash

log_file="exclusoes.log"
find /home/username -type f -size +100k | while read file; do
    echo "Arquivo encontrado: $file"
    echo "Escolha uma opção:"
    echo "1 - Excluir"
    echo "2 - Compactar"
    echo "3 - Ignorar"
    read -p "Digite sua opção (1/2/3): " option

    case $option in
        1)
            echo "$(date) - Excluído: $file" >> "$log_file"
            rm "$file"
            echo "Arquivo excluído: $file"
            ;;
        2)
            gzip "$file"
            echo "Arquivo compactado: $file"
            ;;
        3)
            echo "Ignorando o arquivo: $file"
            ;;
        *)
            echo "Opção inválida!"
            ;;
    esac
done
