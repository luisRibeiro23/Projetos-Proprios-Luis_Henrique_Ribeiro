#!/bin/bash

banner() {
    mensagem="$1"
    declare -A caracteres=(
        [A]="  A  \n A A \nAAAAA\nA   A\nA   A"
        [B]="BBBB \nB   B\nBBBB \nB   B\nBBBB "
        [C]=" CCC \nC    \nC    \nC    \n CCC "
        [D]="DDDD \nD   D\nD   D\nD   D\nDDDD "
        [E]="EEEEE\nE    \nEEE  \nE    \nEEEEE"
        [F]="EEEEE\nE    \nEEE  \nE    \nE    "
        [G]=" GGG \nG    \nG  GG\nG   G\n GGG "
        [H]="H   H\nH   H\nHHHHH\nH   H\nH   H"
        [I]="IIIII\n  I  \n  I  \n  I  \nIIIII"
        [J]="  JJJ\n    J\n    J\nJ   J\n JJJ "
        [K]="K   K\nK  K \nKK   \nK  K \nK   K"
        [L]="L    \nL    \nL    \nL    \nLLLLL"
        [M]="M   M\nMM MM\nM M M\nM   M\nM   M"
        [N]="N   N\nNN  N\nN N N\nN  NN\nN   N"
        [O]=" OOO \nO   O\nO   O\nO   O\n OOO "
        [P]="PPPP \nP   P\nPPPP \nP    \nP    "
        [Q]=" QQQ \nQ   Q\nQ   Q\nQ  QQ\n QQQ "
        [R]="RRRR \nR   R\nRRRR \nR  R \nR   R"
        [S]=" SSS \nS    \n SSS \n    S\nSSSS "
        [T]="TTTTT\n  T  \n  T  \n  T  \n  T  "
        [U]="U   U\nU   U\nU   U\nU   U\n UUU "
        [V]="V   V\nV   V\nV   V\n V V \n  V  "
        [W]="W   W\nW   W\nW M W\nWM WM\nW   W"
        [X]="X   X\n X X \n  X  \n X X \nX   X"
        [Y]="Y   Y\n Y Y \n  Y  \n  Y  \n  Y  "
        [Z]="ZZZZZ\n   Z \n  Z  \n Z   \nZZZZZ"
        [0]=" 000 \n0   0\n0   0\n0   0\n 000 "
        [1]="  1  \n 11  \n  1  \n  1  \n 111 "
        [2]=" 222 \n2   2\n  22 \n2    \n22222"
        [3]="33333\n    3\n 3333\n    3\n33333"
        [4]="4   4\n4   4\n44444\n    4\n    4"
        [5]="55555\n5    \n5555 \n    5\n5555 "
        [6]=" 666 \n6    \n6666 \n6   6\n 666 "
        [7]="77777\n    7\n   7 \n  7  \n  7  "
        [8]=" 888 \n8   8\n 888 \n8   8\n 888 "
        [9]=" 999 \n9   9\n 9999 \n    9\n 999 "
    )
    for ((i=0; i<${#mensagem}; i++)); do
        char=${mensagem:i:1}
        if [[ ${char} =~ [a-zA-Z0-9] ]]; then
            echo -e "${caracteres[${char^^}]}"
        fi
    done
}

banner "$1"
