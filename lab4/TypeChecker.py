import lab4.AST as AST
from lab4.utils import *


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
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

    def visit_String(self, node):
        return StringT

    def visit_Block(self, node):
        self.current_scope = Scope(self.current_scope)
        self.visit(node.stmts)

        return None

    def visit_FnCall(self, node):
        self.visit(node.args)
        if node.fn in ['zeros', 'eye', 'ones']:
            if not 1 <= len(node.args) <= 2:
                print(f"Line {node.line}: wrong number of arguments")
            if all(isinstance(arg, AST.IntNum) for arg in node.args):

                if len(node.args) == 2:
                    return ArrayT(2, FloatT, tuple(arg.value for arg in node.args))
                elif len(node.args) == 1:
                    return ArrayT(2, FloatT, (node.args[0].value, node.args[0].value))

                return ArrayT(2, FloatT, tuple(arg.value for arg in node.args))
            return ArrayT(2, FloatT, (None, None))
        return AnyT

    def visit_Print(self, node):
        self.visit(node.args)
        return None

    def visit_Transposition(self, node):
        type1 = self.current_scope.get(node.target)
        if not isinstance(type1, ArrayT):
            print(f"Line {node.line}: Can't transpose")
            return ArrayT(2, AnyT, (None, None))
        if type1.dims != 2:
            print(f"Line {node.line}: Can't transpose")
            return ArrayT(2, type1.eltype, (None, None))
        m, n = type1.size
        return ArrayT(2, type1.eltype, (n, m))

    def visit_UnaryMinus(self, node):
        type1 = self.visit(node.expr)
        if type1 not in [FloatT, IntT]:
            print(f"Line {node.line}: Can't apply unary minus")
        return type1

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if op[0] == '.':
            op = op[1:]
            if isinstance(type1, ArrayT) and isinstance(type2, ArrayT):
                if type1.size != type2.size:
                    print(f"Line {node.line}: something wrong - .{op}")
                type3 = result_types[op][type1.eltype][type2.eltype]
                if type3 == AnyT:
                    print(
                        f'Line {node.line}: something wrong - {op}')
                return ArrayT(type1.dims, type3, type1.size)
            elif isinstance(type1, ArrayT):
                type3 = result_types[op][type1.eltype][type2]
                if type3 == AnyT:
                    print(
                        f'Line {node.line}: something wrong - {op}')
                return ArrayT(type1.dims, type3, type1.size)
            elif isinstance(type2, ArrayT):
                type3 = result_types[op][type1][type2.eltype]
                if type3 == AnyT:
                    print(
                        f'Line {node.line}: something wrong - {op}')
                return ArrayT(type2.dims, type3, type2.size)
            else:
                print(
                    f'Line {node.line}: something wrong - {op}')
                return AnyT
        else:
            type3 = result_types[op][type1][type2]
            if type3 == AnyT:
                print(
                    f'Line {node.line}: something wrong - {op}')
            return type3

    def visit_Id(self, node):
        type1 = self.current_scope.get(node.id)
        if type1 == None:
            print(f'Line {node.line}: variable not initialized')
            return AnyT
        return type1

    def visit_AssignExpr(self, node):
        type1 = self.visit(node.value)
        if isinstance(node.id, AST.Ref):
            type2 = self.current_scope.get(node.id.target.id)
            if type1 != type2.eltype:
                print(f"Line {node.line}: can't assign")
            return type1
        else:
            self.current_scope.put(node.id.id, type1)
        return type1

    def visit_IfStmt(self, node):
        condt = self.visit(node.cond)
        if condt != BoolT:
            print(f'Line {node.line}: wrong statement')

        self.push_scope()
        self.visit(node.positive)
        self.pop_scope()

        self.push_scope()
        self.visit(node.negative)
        self.pop_scope()

        return None

    def visit_ForLoop(self, node):
        self.loop_count += 1
        type1 = self.visit(node.range)
        if type1 != 'range':
            print(f'Line {node.line}: wrong loop argument')

        self.push_scope()
        self.current_scope.put(node.id, IntT)

        self.visit(node.stmt)

        self.pop_scope()
        self.loop_count -= 1
        return None

    def visit_WhileLoop(self, node):
        self.loop_count += 1

        condt = self.visit(node.cond)
        if condt != BoolT:
            print(f'Line {node.line}: wrong while argument')

        self.push_scope()
        self.visit(node.stmt)
        self.pop_scope()

        self.loop_count -= 1
        return None

    def visit_Range(self, node):
        if not self.visit(node.min) == self.visit(node.max) == IntT:
            print(f"Line {node.line}: wrong range arguments")
        return RangeT

    def visit_Vector(self, node):
        types = list(map(self.visit, node.values))
        eltype = types[0]
        if any(eltype != t for t in types):
            if isinstance(eltype, ArrayT):
                print(f"Line {node.line}: different vector lengths")
                return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
            print(f'Line {node.line}: different vector types')
            return ArrayT(1, AnyT, (len(types),))
        if isinstance(eltype, ArrayT):
            return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
        return ArrayT(1, eltype, (len(types),))

    def visit_Break(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line}: break outside of loop")
        return None

    def visit_Continue(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line}: continue outside of loop")
        return None

    def visit_Ref(self, node):
        targett = self.current_scope.get(node.target.id) if isinstance(node.target, AST.Id) else self.visit(node.target)

        if targett == StringT and len(node.indices) != 1:
            print(f"Line {node.line}: problem with dimensions")
            return IntT
        if isinstance(targett, ArrayT):
            if len(node.indices) != targett.dims:
                print(f"Line {node.line}: problem with dimensions")

            indices = [i.value for i in node.indices]
            if not all(m is None or 1 <= i <= m for i, m in zip(indices, targett.size)):
                print(f"Line {node.line}: Index out of range")
                return targett.eltype

            return targett.eltype
        print(f"Line {node.line}: {targett} is not indexable")
        return AnyT

    def visit_Return(self, node):
        self.visit(node.expr)
        return None

    def push_scope(self):
        self.current_scope = Scope(self.current_scope)

    def pop_scope(self):
        self.current_scope