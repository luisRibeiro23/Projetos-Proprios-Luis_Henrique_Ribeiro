# Trabalho feito por: Nome1 e Nome2

import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprEvalListener import ExprEvalListener
from antlr4.tree.Tree import ParseTreeWalker

def main():
    input_expr = sys.argv[1] if len(sys.argv) > 1 else input("Digite a expressão: ")

    input_stream = InputStream(input_expr)
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.root()

    listener = ExprEvalListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    print("Resultado:", listener.stack[-1])

if __name__ == '__main__':
    main()
