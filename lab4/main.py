
import sys
import ply.yacc as yacc
from lab4.parser import parser
from lab4.scanner import lexer
from lab4.tree_printer import TreePrinter
from lab4.TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    ast = parser.parse(text, lexer=lexer)
    # ast.printTree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)