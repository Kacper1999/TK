import ply.yacc as yacc
from lab2.scanner import *

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', '=', 'SUBASSIGN', 'ADDASSIGN', 'MLPASSIGN', 'DIVASSIGN'),
    ('left', 'EQ', 'NE', '>', 'GOE', '<', 'LOE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMLP', 'DOTDIV')
)


def p_number(p):
    """number : INTNUM
              | FLOATNUM"""


def p_expression(p):
    """expression : ID
                  | number
                  | STRING"""


def p_table(p):
    """table : expression ',' expression
                   | table ',' expression
       expression  : '[' expression ']'
                   | '[' table ']' """


def p_create_matrix(p):
    """expression : ZEROES '(' number ')'
                  | EYE '(' number ')'
                  | ONES '(' number ')' """


def p_negation(p):
    """expression : '-' expression"""


def p_binary_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""


def p_binary_matrix_expression(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMLP expression
                  | expression DOTDIV expression"""


def p_transposition(p):
    """expression : expression TRANSPOSE"""


def p_compare_expression(p): # maybe separate for equal / greater / lower?
    """expression : expression EQ expression
                  | expression NE expression
                  | expression '>' expression
                  | expression GOE expression
                  | expression '<' expression
                  | expression LOE expression"""


def p_range(p):
    """range : expression ':' expression"""


def p_assign_expression(p):
    """instruction : ID '=' expression ';'
                 | ID SUBASSIGN expression ';'
                 | ID ADDASSIGN expression ';'
                 | ID MLPASSIGN expression ';'
                 | ID DIVASSIGN expression ';' """


def p_statements_list(p):
    """statements_list :  statements_list code_block
                        | statements_list instruction
                        | instruction code_block
                        | instruction instruction"""


def p_code_block(p):
    """code_block : expression ';'
                  | '{' statements_list '}'
                  | '{' instruction '}' """


def p_break_continue_statement(p):
    """instruction : BREAK ';'
                  | CONTINUE ';' """


def p_for_loop(p):
    """instruction : FOR ID '=' range code_block
                   | FOR ID '=' range instruction"""


def p_while_loop(p):
    """instruction : WHILE '(' expression ')' code_block
                 | WHILE '(' expression ')' instruction"""


def p_if_else_statement(p):
    """instruction  : IF '(' expression ')' code_block %prec IFX
                  | IF '(' expression ')' code_block else_block
       else_block : ELSE code_block"""


def p_print(p):
    """instruction : PRINT table ';'
                  | PRINT expression ';' """


def p_return_expresion(p):
    """instruction : RETURN ';'
                 | RETURN expression ';' """


def p_error(p):
    if p:
        print("Syntax error at line {0}, Token({1}, '{2}')"
              .format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc(start='statements_list')
