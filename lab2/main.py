import sys
import ply.lex as lex
import lab2.scanner as scanner  # scanner.py is a file you create, (it is not an external library)

import lab2.parser as parser

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = parser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
