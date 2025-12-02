#O programa encontra o primeiro número entre 1 e 10000, em que atenda os requisitos:
#O resto da divisão do número por 5 deve ser igual a 3 (nr % 5 == 3).
#O resto da divisão do número por 7 deve ser igual a 4 (nr % 7 == 4).
#O resto da divisão do número por 9 deve ser igual a 5 (nr % 9 == 5).

#!/bin/bash
MAX=10000
for ((nr = 1; nr < MAX; nr++)); do
  if ((nr % 5 == 3 && nr % 7 == 4 && nr % 9 == 5)); then
    echo "Number = $nr"
    exit 0
  fi
done
exit 1
