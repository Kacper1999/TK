class Node(object):
    pass


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
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Array(Node):
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return str(self.values)


class UnaryMinus(Node):
    def __init__(self, right):
        self.right = right


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignExpr(Node):
    def __init__(self, left, op, right):
        self.left = ID(left)
        self.op = op
        self.right = right


class ForLoop(Node):
    def __init__(self, it, _range, body):
        self.it = it
        self.range = _range
        self.body = body


class WhileLoop(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class IfStmt(Node):
    def __init__(self, cond, body_true, body_false=None):
        self.cond = cond
        self.body_true = body_true
        self.body_false = body_false


class Block(Node):
    def __init__(self, body):
        self.body = body


class Range(Node):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class Transposition(Node):
    def __init__(self, operand):
        self.operand = operand


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Continue(Node):
    def __init__(self):
        pass


class Break(Node):
    def __init__(self):
        pass


class Error(Node):
    def __init__(self, msg):
        self.msg = msg


class MatrixCreation(Node):
    def __init__(self, matrix_type, size):
        self.matrix_type = matrix_type
        self.size = size


class ArrayElement(Node):
    def __init__(self, array_name, index):
        self.array_name = array_name
        self.index = index

    def __repr__(self):
        return f"{self.array_name}[{self.index}]"


class Array2DElement(Node):
    def __init__(self, array_name, row_i, col_i):
        self.array_name = array_name
        self.row_i = row_i
        self.col_i = col_i

    def __repr__(self):
        return f"{self.array_name}[{self.row_i}, {self.col_i}]"


class PrintStmt(Node):
    def __init__(self, to_print):
        self.to_print = to_print
