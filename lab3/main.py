
import sys
import ply.yacc as yacc
from lab3.parser import parser
from lab2.scanner import lexer
from lab3.tree_printer import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example2.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    ast = parser.parse(text, lexer=lexer)
    ast.printTree()