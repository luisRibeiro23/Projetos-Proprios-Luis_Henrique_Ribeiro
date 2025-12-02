#!/bin/bash

for user in $(who | awk '{print $1}' | sort | uniq); do
    real_name=$(grep "^$user:" /etc/passwd | cut -d: -f5)
    last_login=$(lastlog -u $user | awk 'NR==2 {print $4, $5, $6, $7}')
    echo "Usuário: $user"
    echo "Nome real: $real_name"
    echo "Último login: $last_login"
    echo "---------------------------"
done
