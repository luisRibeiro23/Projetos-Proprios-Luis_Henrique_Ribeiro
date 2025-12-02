#!/bin/bash

if [[ "$1" =~ ^-?[0-9]+$ ]]; then
    echo "TRUE"
    exit 0
else
    echo "FALSE"
    exit 1
fi
