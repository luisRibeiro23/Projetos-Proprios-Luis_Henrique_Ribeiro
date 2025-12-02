#!/bin/bash

identificador=$(md5sum /etc/passwd | cut -c 1-6)

echo "Identificador único do computador: $identificador"
