class Node(object):
    def __init__(self, line):
        self.line = line


class IntNum(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class FloatNum(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class ID(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return self.name


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Array(Node):
    def __init__(self, values, line):
        self.values = values
        self.line = line

    def __repr__(self):
        return str(self.values)


class UnaryMinus(Node):
    def __init__(self, right, line):
        self.line = line
        self.right = right
        self.line = line


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class AssignExpr(Node):
    def __init__(self, left, op, right, line):
        self.left = ID(left, line)
        self.op = op
        self.right = right
        self.line = line


class ForLoop(Node):
    def __init__(self, it, _range, body, line):
        self.it = it
        self.range = _range
        self.body = body
        self.line = line


class WhileLoop(Node):
    def __init__(self, cond, body, line):
        self.cond = cond
        self.body = body
        self.line = line


class IfStmt(Node):
    def __init__(self, cond, body_true, line, body_false=None):
        self.cond = cond
        self.body_true = body_true
        self.body_false = body_false
        self.line = line


class Block(Node):
    def __init__(self, body):
        self.body = body


class Range(Node):
    def __init__(self, start, stop, line):
        self.start = start
        self.stop = stop
        self.line = line


class Transposition(Node):
    def __init__(self, operand, line):
        self.operand = operand
        self.line = line


class Return(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line


class Continue(Node):
    pass


class Break(Node):
    pass


class Error(Node):
    def __init__(self, msg):
        self.msg = msg


class MatrixCreation(Node):
    def __init__(self, matrix_type, size, line):
        self.matrix_type = matrix_type
        self.size = size
        self.line = line


class ArrayElement(Node):
    def __init__(self, array_name, index, line):
        self.array_name = array_name
        self.index = index
        self.line = line

    def __repr__(self):
        return f"{self.array_name}[{self.index}]"


class Array2DElement(Node):
    def __init__(self, array_name, row_i, col_i, line):
        self.array_name = array_name
        self.row_i = row_i
        self.col_i = col_i
        self.line = line

    def __repr__(self):
        return f"{self.array_name}[{self.row_i}, {self.col_i}]"


class PrintStmt(Node):
    def __init__(self, to_print):
        self.to_print = to_print
