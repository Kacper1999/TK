import lab4.AST as AST
from collections import defaultdict
from dataclasses import dataclass


class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)


@dataclass
class ArrayT:
    dims: int
    eltype: any
    size: any


AnyT = 'any'
IntT = 'int'
FloatT = 'float'
StringT = 'string'
RangeT = 'range'
BoolT = 'bool'

aaa = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: AnyT
        ))
)

for op in '+-*/':
    aaa[op][IntT][IntT] = IntT
    aaa[op][IntT][FloatT] = FloatT
    aaa[op][FloatT][IntT] = FloatT
    aaa[op][FloatT][FloatT] = FloatT

for op in ['<', '<=', '>', '>=', '!=', '==']:
    aaa[op][IntT][IntT] = BoolT
    aaa[op][IntT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT

for op in ['==', '!=']:
    aaa[op][StringT][StringT] = BoolT


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_scope = Scope()
        self.loop_count = 0

    def visit_IntNum(self, node):
        return IntT

    def visit_FloatNum(self, node):
        return FloatT

    def visit_ID(self, node): #TODO nie działa (powinno po dorobieniu assign
        if self.current_scope.get(node.name) == None:
            print(f'Line {node.line}: ID can not be found in current scope')
            return AnyT
        return type
        return

    def visit_String(self, node):
        return StringT

    def visit_Array(self, node): #TODO
        pass

    def visit_UnaryMinus(self, node):
        if self.visit(node.right) not in [FloatT, IntT]:  # or not isinstance(type1, ArrayT)
            print(f'Line {node.line}: Can\'t apply unary minus to other types than numbers')
        return type

    def visit_BinExpr(self, node): #TODO
        pass

    def visit_AssignExpr(self, node): #TODO
        type1 = self.visit(node.value)
        if isinstance(node.left, AST.Ref):
            # todo A[1,2] =
            type2 = self.current_scope.get(node.id.target.id)
            if type1 != type2.eltype:
                print(f"Line {node.line}: Ref assigment type mismatch {type2.eltype} and {type1}")
            return type1
        else:
            self.current_scope.put(node.left.name, type1)
        return type1

    def visi_ForLoop(self, node): #TODO
        pass

    def visit_WhileLoop(self, node): #TODO
        pass

    def visit_IfStmt(self, node): #TODO
        pass

    def visit_Block(self, node):
        self.current_scope = Scope(self.current_scope)
        self.visit(node.body)
        return None

    def visit_Range(self, node): #TODO
        pass

    def visit_Transposition(self, node): #maybe dodać coś?
        if not type(node.operand) is AST.Array:
            print(f"Line {node.line}: Can not transpose, not a matix")
        return None

    def visit_Return(self, node): #TODO
        self.visit(node.expr)
        return None

    def visit_Continue(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line}: Continue outside loop statement")
        return None

    def visit_Break(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line}: Break outside loop statement")
        return None

    def visit_MatrixCreation(self, node): #TODO
        pass

    def visit_ArrayElement(self, node): #TODO
        pass

    def visit_Array2DElement(self, node): #TODO
        pass

    def visit_PrintStmt(self, node):
        self.visit(node.to_print)
        return None

    def push_scope(self):
        self.current_scope = Scope(self.current_scope)

    def pop_scope(self):
        self.current_scope