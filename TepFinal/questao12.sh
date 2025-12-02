#!/bin/bash
for num in {60000..63000}; do
    is_prime=1
    for ((i=2; i*i<=num; i++)); do
        if ((num % i == 0)); then
            is_prime=0
            break
        fi
    done
    if ((is_prime == 1)); then
        printf "%d " $num
    fi
done
echo
