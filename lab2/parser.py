import ply.yacc as yacc
from lab2.scanner import *

precedence = (
    ('nonassoc', 'IFX'),
    ("nonassoc", "ELSE"),
    ('nonassoc', '=', 'SUBASSIGN', 'ADDASSIGN', 'MLPASSIGN', 'DIVASSIGN'),
    ('left', 'EQ', 'NE', '>', 'GOE', '<', 'LOE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMLP', 'DOTDIV')
)


def p_block(p):
    """
    program : statement
            | program statement
    """


def p_expression(p):
    """expression : ID
            | INTNUM
            | FLOATNUM
            | STRING"""


def p_negation(p):
    """expression : '-' expression"""


def p_binary_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""


def p_transpose(p):
    """expression : expression TRANSPOSE"""


def p_create_matrix(p):
    """expression : ZEROES '(' expression ')'
                  | EYE '(' expression ')'
                  | ONES '(' expression ')' """


def p_assign_expression(p):
    """expression : ID '=' expression
                 | ID SUBASSIGN expression
                 | ID ADDASSIGN expression
                 | ID MLPASSIGN expression
                 | ID DIVASSIGN expression
                 | ID '[' expression ']' '=' expression
                 | ID '[' expression ']' SUBASSIGN expression
                 | ID '[' expression ']' ADDASSIGN expression
                 | ID '[' expression ']' MLPASSIGN expression
                 | ID '[' expression ']' DIVASSIGN expression
                 | ID '[' expression ',' expression ']' '=' expression
                 | ID '[' expression ',' expression ']' SUBASSIGN expression
                 | ID '[' expression ',' expression ']' ADDASSIGN expression
                 | ID '[' expression ',' expression ']' MLPASSIGN expression
                 | ID '[' expression ',' expression ']' DIVASSIGN expression"""


def p_binary_matrix_expression(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMLP expression
                  | expression DOTDIV expression"""


def p_compare_expression(p):
    """expression : expression EQ expression
                  | expression NE expression
                  | expression '>' expression
                  | expression GOE expression
                  | expression '<' expression
                  | expression LOE expression"""


def p_list(p):
    """
    list : expression
         | list ',' expression
    expression : '[' ']'
         | '[' list ']'
    """


def p_statement(p):
    """
    statement : expression ';'
         | print_statement
         | if_statement
         | while_statement
         | for_statement
         | BREAK ';'
         | CONTINUE ';'
         | RETURN expression ';'
         | ';'
         | '{' '}'
         | '{' statement_list '}'
    """


def p_statements_list(p):
    """
        statement_list : statement
                    | statement_list statement
    """


def p_if_statement(p):
    """
    if_statement : IF '(' expression ')' statement %prec IFX
                | IF '(' expression ')' statement ELSE statement
    """


def p_range(p):
    """range : expression ':' expression"""


def p_while_loop(p):
    """
    while_statement : WHILE '(' expression ')' statement

    """


def p_for_loop(p):
    """
    for_statement : FOR ID '=' range statement
    """


def p_print(p):
    """
    print_statement : PRINT statement_list
                    | PRINT list
    """


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()