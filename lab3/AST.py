class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class ID(Node):
    def __init__(self, name):
        self.name = name


class String(Node):
    def __init__(self, value):
        self.value = value


class Array(Node):
    def __init__(self, values):
        self.values = values


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
        self.left = left
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
    def __init__(self, cond, body_true, body_false):
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
