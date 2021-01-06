import ply.yacc as yacc
from lab2.scanner import *
import lab3.AST as ast

precedence = (
    ('nonassoc', 'IFX'),
    ("nonassoc", "ELSE"),
    ('nonassoc', '=', 'SUBASSIGN', 'ADDASSIGN', 'MLPASSIGN', 'DIVASSIGN'),
    ('left', 'EQ', 'NE', '>', 'GOE', '<', 'LOE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMLP', 'DOTDIV'),
    ('left', 'USUB')
)


def p_block(p):
    """
    program : statement
            | program statement
    """
    if len(p) == 2:
        p[0] = ast.Block([p[1]])
    if len(p) == 3:
        p[1].body.append(p[2])
        p[0] = p[1]


def p_id(p):
    """expression : ID"""
    p[0] = ast.ID(p[1])


def p_intnum(p):
    """expression : INTNUM"""
    p[0] = ast.IntNum(p[1])


def p_floatnum(p):
    """expression : FLOATNUM"""
    p[0] = ast.FloatNum(p[1])


def p_string(p):
    """expression : STRING"""
    p[0] = ast.String(p[1])


def p_negation(p):
    """expression : USUB expression"""
    p[0] = ast.UnaryMinus(p[2])


def p_binary_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""
    p[0] = ast.BinExpr(p[2], p[1], p[3])


def p_transpose(p):
    """expression : expression TRANSPOSE"""
    p[0] = ast.Transposition(p[1])


def p_create_matrix(p):
    """expression : ZEROES '(' expression ')'
                  | EYE '(' expression ')'
                  | ONES '(' expression ')' """
    p[0] = ast.MatrixCreation(p[1], p[3])


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
    if len(p) == 4:
        p[0] = ast.AssignExpr(p[1], p[2], p[3])
    elif len(p) == 7:
        array_el = ast.ArrayElement(p[1], p[3])
        p[0] = ast.AssignExpr(array_el, p[5], p[6])
    elif len(p) == 9:
        array_el = ast.Array2DElement(p[1], p[3], p[5])
        p[0] = ast.AssignExpr(array_el, p[7], p[8])


def p_binary_matrix_expression(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMLP expression
                  | expression DOTDIV expression"""
    p[0] = ast.BinExpr(p[2], p[1], p[3])


def p_compare_expression(p):
    """expression : expression EQ expression
                  | expression NE expression
                  | expression '>' expression
                  | expression GOE expression
                  | expression '<' expression
                  | expression LOE expression"""
    p[0] = ast.BinExpr(p[2], p[1], p[3])


def p_array(p):
    """expression : '[' list ']'"""
    p[0] = ast.Array(p[2])


def p_list(p):
    """
    list : expression
         | list ',' expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]


def p_stmt_list(p):
    """statement_list : statement"""
    p[0] = ast.Block([p[1]])


def p_stmt_list_end(p):
    """statement_list : statement_list statement"""
    p[0] = p[1]
    p[0].body.append(p[2])


def p_starting_statement(p):
    """statement : '{' statement_list '}'"""
    p[0] = p[2]


def p_if_statement(p):
    """statement : IF '(' expression ')' statement %prec IFX"""
    p[0] = ast.IfStmt(p[3], p[5])


def p_if_else_statement(p):
    """statement : IF '(' expression ')' statement ELSE statement"""
    p[0] = ast.IfStmt(p[3], p[5], p[7])


def p_print_statement(p):
    """statement : PRINT list ';'"""
    p[0] = ast.PrintStmt(p[2])


def p_range(p):
    """range : expression ':' expression"""
    p[0] = ast.Range(p[1], p[3])


def p_while_loop(p):
    """statement : WHILE '(' expression ')' statement"""
    p[0] = ast.WhileLoop(p[3], p[5])


def p_for_loop(p):
    """statement : FOR ID '=' range statement"""
    p[0] = ast.ForLoop(p[2], p[4], p[5])


def p_break(p):
    """statement : BREAK ';'"""
    p[0] = ast.Break()


def p_continue(p):
    """statement : CONTINUE ';'"""
    p[0] = ast.Continue()


def p_return(p):
    """statement : RETURN expression ';'"""
    p[0] = ast.Return(p[2])


def p_statement(p):
    """statement : expression ';'"""
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()
