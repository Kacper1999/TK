import sys
import lab5.scanner as scanner
from lab5.parser import parser
from tree_printer import TreePrinter
from TypeChecker import TypeChecker
from interpreter import Interpreter
import os

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else os.path.join("examples", "fibonacci.m")
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    Interpreter().visit(ast)
