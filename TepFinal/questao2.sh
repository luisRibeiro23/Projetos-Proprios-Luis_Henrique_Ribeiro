#Este programa renomeia todos os arquivos do diretório atual,
#adicionando ao início de seus nomes a data e hora da última modificação no formato YYYYMMDDHHMMSS.

#!/bin/bash
find -maxdepth 1 -type f -printf '%f\000' | {
  while read -d $'\000'; do
    timestamp=$(date -d "$(stat -c '%y' "$REPLY")" '+%Y%m%d%H%M%S')
    mv "$REPLY" "${timestamp}-$REPLY"
  done
}

