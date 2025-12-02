# Inicializa a variável SUM com o valor 0 e a exporta para o ambiente dos subprocessos
export SUM=0

# Inicia um loop que itera sobre todos os arquivos *.java encontrados no diretório src-name
for f in $(find src-name -name "*.java"); do
  # Conta o número de linhas do arquivo $f usando wc -l e extrai o número de linhas com awk
  # Soma o número de linhas ao valor de SUM
  SUM=$(($SUM + $(wc -l $f | awk '{ print $1 }')))
done

# Exibe o valor final de SUM, que é o total acumulado de linhas de todos os arquivos *.java
echo $SUM

