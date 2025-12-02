#!/bin/bash
# Script para listagem recursiva do diretório inicial e compactação

# Nome do arquivo para salvar a listagem
arquivo="listagem.txt"

# Diretório inicial do usuário
diretorio_inicial="$HOME"

# Criar a listagem recursiva e salvar no arquivo
ls -R "$diretorio_inicial" > "$arquivo"

# Compactar o arquivo usando gzip
gzip -f "$arquivo"

echo "Listagem salva e compactada como ${arquivo}.gz"
