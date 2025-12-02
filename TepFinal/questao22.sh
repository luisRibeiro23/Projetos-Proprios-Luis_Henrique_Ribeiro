#!/bin/bash

# Verificar se o arquivo foi fornecido como argumento
if [ -z "$1" ]; then
    echo "Erro: forneça o arquivo de dados como argumento."
    exit 1
fi

# Definir o arquivo de dados
ARQUIVO="$1"

# Inicializar variáveis
total_geral=0
num_contribuintes=0
menor_contribuicao=9999999
maior_contribuicao=-1

# Cabeçalho do relatório
echo "Nome do Candidato        Telefone         Janeiro   Fevereiro Março    Total"
echo "-------------------------------------------------------------"

# Ler cada linha do arquivo de dados
while IFS=: read -r nome telefone jan fev mar; do
    # Calcular o total das contribuições
    total=$(echo "$jan + $fev + $mar" | bc)

    # Atualizar o total geral e o número de contribuintes
    total_geral=$(echo "$total_geral + $total" | bc)
    num_contribuintes=$((num_contribuintes + 1))

    # Verificar o menor e maior valor de contribuição
    if (( $(echo "$jan < $menor_contribuicao" | bc -l) )); then
        menor_contribuicao=$jan
    fi
    if (( $(echo "$fev < $menor_contribuicao" | bc -l) )); then
        menor_contribuicao=$fev
    fi
    if (( $(echo "$mar < $menor_contribuicao" | bc -l) )); then
        menor_contribuicao=$mar
    fi

    if (( $(echo "$jan > $maior_contribuicao" | bc -l) )); then
        maior_contribuicao=$jan
    fi
    if (( $(echo "$fev > $maior_contribuicao" | bc -l) )); then
        maior_contribuicao=$fev
    fi
    if (( $(echo "$mar > $maior_contribuicao" | bc -l) )); then
        maior_contribuicao=$mar
    fi

    # Exibir a linha de contribuição do candidato
    printf "%-24s %-15s %8.2f %8.2f %8.2f %8.2f\n" "$nome" "$telefone" "$jan" "$fev" "$mar" "$total"
done < "$ARQUIVO"

# Calcular a média de contribuições
media=$(echo "$total_geral / $num_contribuintes" | bc -l)

# Relatório final
echo "-------------------------------------------------------------"
printf "Total recebido: %.2f\n" "$total_geral"
printf "Contribuição média: %.2f\n" "$media"
printf "Menor contribuição: %.2f\n" "$menor_contribuicao"
printf "Maior contribuição: %.2f\n" "$maior_contribuicao"
