
import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprEvalVisitor import ExprEvalVisitor

def main():
    input_expr = sys.argv[1] if len(sys.argv) > 1 else input("Digite a expressão: ")

    input_stream = InputStream(input_expr)
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.root()

    visitor = ExprEvalVisitor()
    result = visitor.visit(tree)

    print("Resultado:", result)

if __name__ == '__main__':
    main()
