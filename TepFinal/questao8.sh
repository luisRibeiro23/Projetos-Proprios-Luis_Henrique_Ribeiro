#!/bin/bash

read -p "Digite uma string: " input

reversa=$(echo "$input" | rev)


echo "String invertida: $reversa"
