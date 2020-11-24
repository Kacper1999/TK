from __future__ import print_function
import lab3.AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("| " * indent, self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent, self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent, self.value)

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        print("| " * indent, self.values)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print("| " * indent, self.name)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print("| " * indent, self.msg)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for stmt in self.body:
            stmt.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print("| " * indent, "-")
        self.right.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent, self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("| " * indent, self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("| " * indent, "FOR")
        print("| " * (indent + 1), self.it)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print("| " * indent, "WHILE")
        self.cond.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.IfStmt)
    def printTree(self, indent=0):
        print("| " * indent, "IF")
        self.cond.printTree(indent + 1)
        print("| " * indent, "THEN")
        self.body_true.printTree(indent + 1)
        if self.body_false:
            print("| " * indent, "ELSE")
            self.body_false.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("| " * indent, "RANGE")
        print("| " * (indent + 1), self.start)
        print("| " * (indent + 1), self.stop)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print("| " * indent, "TRANSPOSITION")
        self.operand.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("| " * indent, "RETURN")
        self.expr.printTree(indent + 1)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("| " * indent, "CONTINUE")

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("| " * indent, "BREAK")
