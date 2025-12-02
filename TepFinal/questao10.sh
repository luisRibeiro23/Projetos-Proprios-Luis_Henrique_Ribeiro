#!/bin/bash
find /home/seu-nome -type f -mtime -1 | tar -czvf arquivos_modificados.tar.gz -T -
