import ply.lex as lex

tokens = (
    # 'PLUS',
    # 'MINUS',
    # 'TIMES',
    # 'DIVIDE',
    'DOTADD',
    'DOTSUB',
    'DOTMLP',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MLPASSIGN',
    'DIVASSIGN',
    'TRANSPOSE',
    'GOE',
    'LOE',
    'NE',
    'EQ',
    'INTNUM',
    'FLOATNUM',
    'STRING',
    'ID',
)
t_DOTADD = r'.\+'
t_DOTSUB = r'.\-'
t_DOTMLP = r'.\*'
t_DOTDIV = r'./'
t_TRANSPOSE = r"'"

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'\-='
t_MLPASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_GOE = r'>='
t_LOE = r'<='
t_NE = r'!='
t_EQ = r'=='

literals = ['+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ',', ';', ':', '>', '<']
# literals = r"+-/*=<>()[]{}:',;"

t_ignore = ' \t'

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'zeros': 'ZEROES',
    'ones': 'ONES',
    'eye': 'EYE',
    'print': 'PRINT'
}

tokens += tuple(reserved.values())


def t_FLOATNUM(t):
    r"""(\d*\.\d+([eE][-+]?\d+)?)|(\d+\.\d*([eE][-+]?\d+)?)"""
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_ID(t):
    r"""[a-zA-Z_][\w_]*"""
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t



def t_COMMENT(t):
    r"""\#.*"""
    pass


def t_STRING(t):
    r"""\".*?\""""
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
# fh = open("example.txt")
# lexer.input(fh.read())
# for token in lexer:
#     print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
